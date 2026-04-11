import requests

def fetch_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        
        data = res.json()
        if data.get("status") == 1:
            product = data.get("product", {})
            return {
                "name": product.get("product_name"),
                "category": product.get("categories"),
                "price": product.get("price"),
                "quantity": product.get("quantity"),
                "barcode": barcode,
                "brand": product.get("brands"),
                "ingredients": product.get("ingredients_text"),
                "description": product.get("generic_name")
            }
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
    
    return None