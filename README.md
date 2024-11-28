## README

### Product Matcher

This script allows you to match unclean product data to a clean product catalog using LM Studio API.

### Requirements

- Python 3.x
- `requests` library
- `pandas` library

Install the required libraries using:

```bash
pip install requests pandas
```

### Usage

```bash
python product_matcher.py --catalog path_to_catalog.csv --input 'JSON_input'
```

or

```bash
python product_matcher.py --catalog path_to_catalog.csv --input-file path_to_input.json
```

- `--catalog`: Path to the product catalog CSV file.
- `--input`: Unclean product data in JSON format.
- `--input-file`: Path to input JSON file containing an array of unclean product data.

**Note:** You must provide either `--input` or `--input-file`, but not both.

### Examples

#### Single Input Example

```bash
python product_matcher.py --catalog product_catalog.csv --input '{"ProductID": "SBD-PT-02", "ProductName": "Circular Saw 15Amp 7-1/4in"}'
```

#### Input File Example

Create a JSON file named `unclean_products.json` with the following content:

```json
[
  { "ProductID": "SBD-PT-02", "ProductName": "Circular Saw 15Amp 7-1/4in" },
  { "ProductID": "SBD-AC-003", "ProductName": "14-Piece Drill Bit Set" },
  { "ProductID": "SBD-HT-006", "ProductName": "10 in. Adjustable Wrench" },
  { "ProductID": null, "ProductName": "10 in. Adjustable Wrench" },
  { "ProductID": "Null", "ProductName": "10 in. Adjustable Wrench" }
]
```

Then run:

```bash
python product_matcher.py --catalog product_catalog.csv --input-file unclean_products.json
```


### Output

The output will be printed to the screen in JSON format. For example:

```json
{
  "user_message": {
    "ProductID": "SBD-PT-02",
    "ProductName": "Circular Saw 15Amp 7-1/4in"
  },
  "assistant_response": "{\n  \"CanonicalProductID\": \"SBD-PT-002\",\n  \"ConfidenceScore\": 0.95\n}"
}
```

When using `--input-file`, the output will be a JSON array of results.

### Notes

- Replace `"llama-3b-instruct"` in the script with your actual model name if different.
- Ensure that the model is running and accessible at `http://localhost:1234/v1/chat/completions`.
- You can redirect the output to a file if needed:

  ```bash
  python product_matcher.py --catalog product_catalog.csv --input-file unclean_products.json > results.json
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

