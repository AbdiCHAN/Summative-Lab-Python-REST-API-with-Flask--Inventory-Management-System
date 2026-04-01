import requests

def fetch_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        if data["status"] == 1:
            product = data["product"]
            return {
                "name": product.get("product_name"),
                "brand": product.get("brands"),
                "ingredients": product.get("ingredients_text")
            }
    return None