import argparse
import requests
import json
import pandas as pd
import sys

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Product matching using LM Studio API')
    parser.add_argument('--catalog', type=str, required=True, help='Path to the product catalog CSV file')
    parser.add_argument('--input', type=str, help='Single input in JSON array format')
    parser.add_argument('--input-file', type=str, help='Path to input JSONL file containing arrays of messages')
    parser.add_argument('--output-file', type=str, required=True, help='Path to output JSONL file to save results')
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

    # Prepare the system message
    system_message = {
        "role": "system",
        "content": f"""
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

**Function Definition:**

{function_definition}

Here is the product catalog in CSV format:

{catalog_csv}
"""
    }

    # Prepare list of inputs
    if args.input:
        try:
            input_data = json.loads(args.input)
            if not isinstance(input_data, list):
                print("Error: Input must be a JSON array of messages.")
                sys.exit(1)
            inputs = [input_data]
        except json.JSONDecodeError as e:
            print(f"Error parsing input JSON: {e}")
            sys.exit(1)
    else:
        inputs = []
        try:
            with open(args.input_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        input_data = json.loads(line)
                        if not isinstance(input_data, list):
                            print("Error: Each line in the input file must be a JSON array of messages.")
                            continue  # Skip this line
                        inputs.append(input_data)
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)

    # Open the output file
    with open(args.output_file, 'w') as output_file:
        # Process each input
        for input_data in inputs:
            # Extract the user message from the input array
            user_message = None
            for message in input_data:
                if message.get("role") == "user":
                    user_message = message
                    break
            if not user_message:
                print("Error: No user message found in the input.")
                continue  # Skip this entry

            # Build the conversation messages
            messages = [system_message, user_message]

            # Set up the request payload
            payload = {
                "model": "llama-3b-instruct",  # Replace with your model name if different
                "messages": messages
            }

            # Send the request to the LM Studio API
            try:
                response = requests.post(
                    "http://localhost:1234/v1/chat/completions",
                    headers={
                        "Content-Type": "application/json",
                    },
                    data=json.dumps(payload)
                )
            except requests.exceptions.RequestException as e:
                print(f"Error connecting to LM Studio API: {e}")
                sys.exit(1)

            # Check if the response is successful
            if response.status_code == 200:
                response_data = response.json()
                # Extract the assistant's message
                assistant_message = response_data['choices'][0]['message']
                conversation = [system_message, user_message, assistant_message]
                # Output the conversation as a single line JSON array
                output_file.write(json.dumps(conversation) + '\n')
            else:
                error_message = {
                    "role": "assistant",
                    "content": f"Error: {response.status_code} {response.text}"
                }
                conversation = [system_message, user_message, error_message]
                # Output the conversation as a single line JSON array
                output_file.write(json.dumps(conversation) + '\n')

if __name__ == "__main__":
    main()
