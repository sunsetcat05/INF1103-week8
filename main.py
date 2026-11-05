import json
from pathlib import Path

from Inventory import Inventory, DATA_FILE
from physical_products import PhysicalProduct
from digital_products import DigitalProduct


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def print_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Load inventory")
    print("7. Exit")


def add_product_menu(inventory):
    product_id = read_text("Product ID: ")
    if inventory.find_product(product_id) is not None:
        print("A product with that ID already exists.")
        return
    name = read_text("Name: ")
    price = read_float("Price: ")
    stock = read_int("Stock quantity: ")

    choice = ""
    while choice not in ("1", "2"):
        choice = input("Product type (1 = Physical, 2 = Digital): ").strip()

    try:
        if choice == "1":
            weight = read_float("Weight (kg): ")
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            size = read_float("Download size (MB): ")
            product = DigitalProduct(product_id, name, price, stock, size)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return

    inventory.add_product(product)
    print(f"Added: {name}")
    print(product.get_fulfilment_info())


def update_stock_menu(inventory):
    product_id = read_text("Product ID: ")
    change = read_int("Stock change (positive to add, negative to remove): ")
    try:
        if inventory.update_stock(product_id, change):
            print("Stock updated.")
        else:
            print("Product not found.")
    except ValueError as error:
        print(f"Could not update stock: {error}")


def search_menu(inventory):
    keyword = read_text("Search by name or ID: ")
    results = inventory.search(keyword)
    if not results:
        print("No matching products.")
        return
    for product in results:
        product.display_information()
        print()


def save_inventory(inventory):
    inventory.save_to_file()
    print(f"Saved {len(inventory)} product(s) to {DATA_FILE}.")


def load_inventory(inventory):
    try:
        count = inventory.load_from_file()
        print(f"Loaded {count} product(s) from {DATA_FILE}.")
    except FileNotFoundError:
        print(f"No saved file found ({DATA_FILE}).")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Could not load data: {error}")


def main():
    inventory = Inventory()
    if Path(DATA_FILE).exists():
        load_inventory(inventory)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_menu(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            load_inventory(inventory)
        elif choice == "7":
            if input("Save before exiting? (y/n): ").strip().lower() == "y":
                save_inventory(inventory)
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-7.")


if __name__ == "__main__":
    main()