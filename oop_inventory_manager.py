import json

FILENAME = "inventory.json"


class Product:
    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.update_stock(stock)   # reuses the stock validation

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_id()) is not None:
            raise ValueError(f"Product ID {product.get_id()} already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_id() == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 50)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 50)

    def to_list(self):
        return [product.to_dict() for product in self.__products]


def load_default_products(inventory):
    inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
    inventory.add_product(Product("P002", "Mouse", 25.50, 40))
    inventory.add_product(Product("P003", "Keyboard", 45.00, 25))


def load_inventory(inventory):
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
        items = data["inventory"] if isinstance(data, dict) else data
        for item in items:
            inventory.add_product(
                Product(item["id"], item["name"], item["price"], item["stock"])
            )
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("Inventory file not found. Starting with default products.")
        load_default_products(inventory)


def save_inventory(inventory):
    with open(FILENAME, "w") as file:
        json.dump({"inventory": inventory.to_list()}, file, indent=4)
    print(f"Inventory saved to {FILENAME}.")


def handle_add_product(inventory):
    product_id = input("Product ID: ")
    name = input("Product Name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        inventory.add_product(Product(product_id, name, price, stock))
        print("Product added successfully!")
    except ValueError as error:
        print(f"Could not add product: {error}")


def handle_update_stock(inventory):
    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print(f"\nProduct Found: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        product.update_stock(int(input("\nNew Stock Quantity: ")))
        print("Stock updated successfully!")
    except ValueError as error:
        print(f"Could not update stock: {error}")


def handle_search(inventory):
    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        print("\nProduct Found")
        product.display_information()


def main():
    inventory = Inventory()
    load_inventory(inventory)

    while True:
        print("--------------Menu--------------")
        print("1. Display All Products")
        print("2. Add New Product")
        print("3. Update Stock Quantity")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("--------------------------------")
        choice = input("\nEnter option: ")

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            handle_add_product(inventory)
        elif choice == "3":
            handle_update_stock(inventory)
        elif choice == "4":
            handle_search(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit.....")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()