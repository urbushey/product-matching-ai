Here's the updated README with the updated output format. The script will now generate outputs in the ChatGPT-compatible format with `system`, `user`, and `assistant` messages.

---

## README

### Product Matcher

This script allows you to match unclean product data to a clean product catalog using LM Studio API or a similar API that supports the ChatGPT API format. 

### Requirements

- Python 3.x
- `requests` library
- `pandas` library
- LM Studio (or another tool that can run an LLM server locally using the ChatGPT API format)

Install the required libraries using:

```bash
pip install requests pandas
```

### Usage

```bash
python scripts/llama_product_inference.py --catalog catalogs/path_to_catalog.csv --input 'JSON_input'
```

or

```bash
python scripts/llama_product_inference.py --catalog catalogs/hardware.csv --input-file unclean/test1.json
```

- `--catalog`: Path to the product catalog CSV file.
- `--input`: Unclean product data in JSON format (must follow the `role` and `content` structure).
- `--input-file`: Path to input JSON file containing an array of unclean product data, each as an object in `role` and `content` format.

**Note:** You must provide either `--input` or `--input-file`, but not both.

### Examples

#### Single Input Example

```bash
python scripts/llama_product_inference.py --catalog catalogs/hardware.csv --input '{"role": "user", "content": "[{ "ProductID": "SBD-PT-02", "ProductName": "Circular Saw 15Amp 7-14in" }]"}'
```

#### Input File Example

Create a JSON file named `unclean_products.json` with the following content:

```json
[
  { "role": "user", "content": "Match the following product: { \"ProductID\": \"SBD-PT-02\", \"ProductName\": \"Circular Saw 15Amp 7-1/4in\" }" },
  { "role": "user", "content": "Match the following product: { \"ProductID\": \"SBD-AC-003\", \"ProductName\": \"14-Piece Drill Bit Set\" }" },
  { "role": "user", "content": "Match the following product: { \"ProductID\": \"SBD-HT-006\", \"ProductName\": \"10 in. Adjustable Wrench\" }" },
  { "role": "user", "content": "Match the following product: { \"ProductID\": null, \"ProductName\": \"10 in. Adjustable Wrench\" }" },
  { "role": "user", "content": "Match the following product: { \"ProductID\": \"Null\", \"ProductName\": \"10 in. Adjustable Wrench\" }" }
]
```

Then run:

```bash
python scripts/llama_product_inference.py --catalog catalog/product_catalog.csv --input-file unclean/unclean_products.json
```

### Output

The output will be printed to the screen in JSON format as an array of messages in the ChatGPT format, with `system`, `user`, and `assistant` roles. For example:

```json
[
  {
    "role": "system",
    "content": "You are an assistant that matches unclean product data to a clean product catalog."
  },
  {
    "role": "user",
    "content": "Match the following product: { \"ProductID\": \"SBD-PT-02\", \"ProductName\": \"Circular Saw 15Amp 7-1/4in\" }"
  },
  {
    "role": "assistant",
    "content": "{ \"CanonicalProductID\": \"SBD-PT-002\", \"ConfidenceScore\": 0.95 }"
  }
]
```

When using `--input-file`, the output will include an array of message sets for all provided inputs.

### Notes

- Replace `"llama-3b-instruct"` in the script with your actual model name if different.
- Ensure that the model is running and accessible at `http://localhost:1234/v1/chat/completions`.
- You can redirect the output to a file if needed:

  ```bash
  python llama_product_inference.py --catalog product_catalog.csv --input-file unclean_products.json > results.json
  ```

---

**Sample product catalog (product_catalog.csv):**

```
Canonical Product ID,Product Name,Product Category
SBD-PT-001,"20V MAX* Cordless Drill/Driver Kit (1.5 Ah)",Power Tools
SBD-PT-002,"15 Amp 7-1/4 in. Corded Circular Saw",Power Tools
SBD-PT-003,"18V Cordless Impact Driver",Power Tools
SBD-AC-003,"14-Piece Drill Bit Set",Accessories
SBD-HT-006,"10 in. Adjustable Wrench",Hand Tools
```

**Ensure the product catalog CSV file is correctly formatted and matches the sample data provided.**
```
