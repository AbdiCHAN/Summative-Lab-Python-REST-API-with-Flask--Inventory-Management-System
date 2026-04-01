import requests

BASE = "http://127.0.0.1:5000"

while True:
    print("\n1.Add 2.View 3.Update 4.Delete 5.Fetch API 6.Exit")
    choice = input("Choice: ")

    if choice == "1":
        data = {
            "id": int(input("ID: ")),
            "name": input("Name: "),
            "price": float(input("Price: "))
        }
        print(requests.post(f"{BASE}/inventory", json=data).json())

    elif choice == "2":
        print(requests.get(f"{BASE}/inventory").json())

    elif choice == "3":
        id = input("ID: ")
        price = float(input("New Price: "))
        print(requests.patch(f"{BASE}/inventory/{id}", json={"price": price}).json())

    elif choice == "4":
        id = input("ID: ")
        requests.delete(f"{BASE}/inventory/{id}")

    elif choice == "5":
        code = input("Barcode: ")
        print(requests.get(f"{BASE}/fetch/{code}").json())

    elif choice == "6":
        break