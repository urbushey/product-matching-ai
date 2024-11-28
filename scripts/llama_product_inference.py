import argparse
import requests
import json
import pandas as pd

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Product matching using LM Studio API')
    parser.add_argument('--catalog', type=str, required=True, help='Path to the product catalog CSV file')
    parser.add_argument('--input', type=str, required=True, help='Unclean product data in JSON format')
    args = parser.parse_args()

    # Read the product catalog CSV file
    catalog_df = pd.read_csv(args.catalog)

    # Convert the catalog to CSV format as a string without index
    catalog_csv = catalog_df.to_csv(index=False)

    # Get the unclean product data from the input argument
    unclean_product_data = json.loads(args.input)

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

    # Construct the prompt
    prompt = f"""
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

**Unclean Product Data:**

{json.dumps(unclean_product_data, indent=2)}
"""

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
        print(assistant_message)
    else:
        print(f"Error: {response.status_code} {response.text}")

if __name__ == "__main__":
    main()
