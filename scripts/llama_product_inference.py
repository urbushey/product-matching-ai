import argparse
import requests
import json
import pandas as pd
import sys

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Product matching using LM Studio API')
    parser.add_argument('--catalog', type=str, required=True, help='Path to the product catalog CSV file')
    parser.add_argument('--input', type=str, help='Unclean product data in JSON format')
    parser.add_argument('--input-file', type=str, help='Path to input JSON file containing unclean product data array')
    args = parser.parse_args()

    # Check that either --input or --input-file is provided
    if not args.input and not args.input_file:
        print("Error: You must provide either --input or --input-file")
        sys.exit(1)
    if args.input and args.input_file:
        print("Error: Please provide only one of --input or --input-file")
        sys.exit(1)

    # Read the product catalog CSV file
    catalog_df = pd.read_csv(args.catalog)

    # Convert the catalog to CSV format as a string without index
    catalog_csv = catalog_df.to_csv(index=False)

    # Function definition as JSON Schema
    function_definition = '''
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "MatchProductFunction",
      "description": "Schema for the match_product function that matches an unclean product to the canonical product catalog.",
      "type": "object",
      "properties": {
        "CanonicalProductID": {
          "type": "string",
          "description": "The Canonical Product ID that best matches the unclean product."
        },
        "ConfidenceScore": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Confidence score between 0 (low confidence) and 1 (high confidence)."
        }
      },
      "required": ["CanonicalProductID", "ConfidenceScore"],
      "additionalProperties": false
    }
    '''

    # Prepare the base prompt (without unclean product data)
    base_prompt = f"""
You are an assistant that matches unclean product data to a clean product catalog.

**Task:**

- Match the unclean product data to the most appropriate `CanonicalProductID` from the catalog.
- Always provide a `CanonicalProductID`, even if the match has low confidence.
- Provide a `ConfidenceScore` between 0 and 1 indicating the confidence level of the match.
- Do not include any additional text or explanations.
- Provide your answer by calling the function `match_product` with the appropriate parameters in valid JSON format.

**Instructions:**

- Focus on matching primarily based on `ProductName`.
- Consider the `ProductID` in the unclean data as potentially unreliable.
- If the best match is uncertain, reflect this with a low `ConfidenceScore`.

Here is the product catalog in CSV format:

{catalog_csv}

**Function Definition:**

{function_definition}
"""

    # Prepare list of unclean product data entries
    if args.input:
        try:
            unclean_products = [json.loads(args.input)]
        except json.JSONDecodeError as e:
            print(f"Error parsing input JSON: {e}")
            sys.exit(1)
    else:
        try:
            with open(args.input_file, 'r') as f:
                unclean_products = json.load(f)
            if not isinstance(unclean_products, list):
                print("Error: The input JSON file must contain an array of unclean product data.")
                sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)

    # Process each unclean product data entry
    results = []
    for unclean_product_data in unclean_products:
        # Create the prompt by adding the unclean product data to the base prompt
        prompt = base_prompt + f"\n**Unclean Product Data:**\n\n{json.dumps(unclean_product_data, indent=2)}\n"

        # Set up the request payload
        payload = {
            "model": "llama-3b-instruct",  # Replace with your model name if different
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        # Send the request to the LM Studio API
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(payload)
        )

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            # Extract the assistant's message
            assistant_message = response_data['choices'][0]['message']['content']
            result = {
                "user_message": unclean_product_data,
                "assistant_response": assistant_message
            }
            results.append(result)
        else:
            error_message = f"Error: {response.status_code} {response.text}"
            result = {
                "user_message": unclean_product_data,
                "assistant_response": error_message
            }
            results.append(result)

    # Print the results
    if args.input:
        print(json.dumps(results[0], indent=2))
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
