import requests
import csv

# 🔧 EDIT THESE TWO LINES
STORE_ID = "ECWID_STORE_ID"          # e.g., "42429290"
SECRET_TOKEN = "ECWID_SECRET_TOKEN"  # e.g., "secret_XXXXXXXX"

API_URL = f"https://app.ecwid.com/api/v3/{STORE_ID}/products"
HEADERS = {
    "Authorization": f"Bearer {SECRET_TOKEN}"
}

def fetch_all_products():
    items = []
    offset = 0
    limit = 100

    while True:
        params = {
            "offset": offset,
            "limit": limit
        }
        resp = requests.get(API_URL, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()

        batch = data.get("items", [])
        items.extend(batch)

        if len(batch) < limit:
            break

        offset += limit

    return items

def write_csv(products, filename="google_feed.csv"):
    # Basic Google Merchant-style columns
    fieldnames = [
        "id",
        "title",
        "description",
        "link",
        "image_link",
        "price",
        "availability",
        "condition"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p in products:
            product_id = p.get("id")
            name = p.get("name", "")
            description = p.get("description", "")
            url = p.get("url", "")
            image = p.get("imageUrl", "")
            price = p.get("price", 0)

            row = {
                "id": product_id,
                "title": name,
                "description": description,
                "link": url,
                "image_link": image,
                "price": f"{price} USD",   # adjust currency if needed
                "availability": "in stock" if p.get("inStock", True) else "out of stock",
                "condition": "new"
            }
            writer.writerow(row)

def main():
    print("Fetching products from Ecwid...")
    products = fetch_all_products()
    print(f"Fetched {len(products)} products.")

    print("Writing google_feed.csv...")
    write_csv(products)
    print("Done. File saved as google_feed.csv")

if __name__ == "__main__":
    main()
