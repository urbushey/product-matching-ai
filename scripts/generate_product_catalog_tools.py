import random
import csv
import os
from faker import Faker

# Initialize Faker for generating random product details
fake = Faker()

# Define default tool categories and their product types
DEFAULT_CATEGORIES = {
    "Hand Tools": ["Hammer", "Screwdriver", "Wrench", "Pliers"],
    "Power Tools": ["Drill", "Circular Saw", "Sander", "Grinder"],
    "Outdoor Tools": ["Lawnmower", "Chainsaw", "Hedge Trimmer", "Leaf Blower"],
}

# Function to generate a product catalog
def generate_product_catalog(
    output_file="product_catalog.csv",
    num_products=100,
    categories=DEFAULT_CATEGORIES,
):
    """Generates a CSV product catalog with random tool products.

    Args:
        output_file (str): Path to save the CSV file.
        num_products (int): Number of products to generate.
        categories (dict): A dictionary of categories and their product types.
    """
    # Prepare the data structure
    products = []
    category_keys = list(categories.keys())

    for _ in range(num_products):
        # Randomly choose a category and product type
        category = random.choice(category_keys)
        product_type = random.choice(categories[category])

        # Generate random details for the product
        product_id = fake.unique.uuid4()
        product_name = f"{fake.word().capitalize()} {product_type}"
        product_description = fake.sentence(nb_words=12)
        sku_number = fake.unique.ean8()
        upc = fake.unique.ean13()

        # Append to the list
        products.append(
            {
                "Product ID": product_id,
                "Product Name": product_name,
                "Product Category": category,
                "Product Description": product_description,
                "SKU Number": sku_number,
                "UPC": upc,
            }
        )

    # Write the products to a CSV file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=products[0].keys(), delimiter=","
        )
        writer.writeheader()
        writer.writerows(products)

    print(f"Generated product catalog with {num_products} products at: {output_file}")

# Run the script
if __name__ == "__main__":
    # Configurable parameters
    OUTPUT_FILE = "data/sample_catalogs/product_catalog.csv"
    NUM_PRODUCTS = 100
    CATEGORIES = {
        "Hand Tools": ["Screwdriver", "Hammer", "Wrench"],
        "Power Tools": ["Drill", "Impact Driver"],
        "Storage": ["Toolbox", "Cabinet"],
    }

    # Generate the catalog
    generate_product_catalog(
        output_file=OUTPUT_FILE, num_products=NUM_PRODUCTS, categories=CATEGORIES
    )
