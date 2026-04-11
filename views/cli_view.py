import requests
import json

BASE = "http://127.0.0.1:5000/products"

def display_menu():
    print("\n=== Inventory Management System ===")
    print("1. Add Product")
    print("2. View All Products")
    print("3. View Product by ID")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Search Products by Name")
    print("7. Filter Products by Category")
    print("8. Get Inventory Statistics")
    print("9. Fetch Product from API")
    print("10. Save Fetched Product")
    print("11. Exit")

def add_product():
    print("\n--- Add Product ---")
    data = {
        "name": input("Name: "),
        "category": input("Category: "),
        "price": float(input("Price: ")),
        "quantity": int(input("Quantity: ")),
        "barcode": input("Barcode: "),
        "brand": input("Brand: "),
        "ingredients": input("Ingredients: "),
        "description": input("Description: ")
    }
    res = requests.post(BASE, json=data)
    print(res.json())

def view_all():
    print("\n--- All Products ---")
    res = requests.get(BASE)
    products = res.json()
    for product in products:
        print(json.dumps(product, indent=2))

def view_by_id():
    print("\n--- View Product ---")
    item_id = int(input("Product ID: "))
    res = requests.get(f"{BASE}/{item_id}")
    print(res.json())

def update_product():
    print("\n--- Update Product ---")
    item_id = int(input("Product ID: "))
    data = {
        "price": float(input("New Price: ")),
        "quantity": int(input("New Quantity: "))
    }
    res = requests.patch(f"{BASE}/{item_id}", json=data)
    print(res.json())

def delete_product():
    print("\n--- Delete Product ---")
    item_id = int(input("Product ID: "))
    res = requests.delete(f"{BASE}/{item_id}")
    print(res.status_code)

def search_products():
    print("\n--- Search Products ---")
    name = input("Search name: ")
    res = requests.get(f"{BASE}/search?name={name}")
    products = res.json()
    for product in products:
        print(json.dumps(product, indent=2))

def filter_products():
    print("\n--- Filter Products ---")
    category = input("Category: ")
    res = requests.get(f"{BASE}?category={category}")
    products = res.json()
    for product in products:
        print(json.dumps(product, indent=2))

def get_stats():
    print("\n--- Inventory Statistics ---")
    res = requests.get(f"{BASE}/stats")
    print(res.json())

def fetch_product():
    print("\n--- Fetch Product from API ---")
    barcode = input("Barcode: ")
    res = requests.get(f"{BASE}/fetch/{barcode}")
    print(res.json())

def save_fetched_product():
    print("\n--- Save Fetched Product ---")
    barcode = input("Barcode: ")
    res = requests.post(f"{BASE}/fetch", json={"barcode": barcode})
    print(res.json())

def main():
    while True:
        display_menu()
        choice = input("Choice: ")
        
        if choice == "1":
            add_product()
        elif choice == "2":
            view_all()
        elif choice == "3":
            view_by_id()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            search_products()
        elif choice == "7":
            filter_products()
        elif choice == "8":
            get_stats()
        elif choice == "9":
            fetch_product()
        elif choice == "10":
            save_fetched_product()
        elif choice == "11":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()