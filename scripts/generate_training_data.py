import csv
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate dataset for product matching.')
    parser.add_argument('--catalog', type=str, required=True, help='Path to the product catalog CSV file')
    parser.add_argument('--input-file', type=str, default='canonical_inputs.jsonl', help='Output file for generated inputs in JSONL format')
    parser.add_argument('--output-file', type=str, default='canonical_outputs.jsonl', help='Output file for expected outputs in JSONL format')
    args = parser.parse_args()

    # Read the product catalog CSV file
    with open(args.catalog, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        catalog = [row for row in reader]

    # Open the input and output files
    with open(args.input_file, 'w', encoding='utf-8') as f_input, open(args.output_file, 'w', encoding='utf-8') as f_output:
        # Generate inputs and expected outputs
        for product in catalog:
            # Use exact product data as unclean product data
            unclean_product_data = {
                "ProductID": product['Canonical Product ID'],
                "ProductName": product['Product Name']
            }
            # Create the user message
            user_message = {
                "role": "user",
                "content": json.dumps(unclean_product_data)
            }
            # Create the input conversation (only user message)
            input_conversation = [user_message]
            # Write the input conversation to the input file as a single line
            f_input.write(json.dumps(input_conversation) + '\n')

            # Expected assistant response
            assistant_response = {
                "role": "assistant",
                "content": json.dumps({
                    "CanonicalProductID": product['Canonical Product ID'],
                    "ConfidenceScore": 1.0
                })
            }
            # Create the output conversation (user message and assistant response)
            output_conversation = [user_message, assistant_response]
            # Write the output conversation to the output file as a single line
            f_output.write(json.dumps(output_conversation) + '\n')

    print(f"Canonical inputs saved to {args.input_file}")
    print(f"Canonical outputs saved to {args.output_file}")

if __name__ == "__main__":
    main()
