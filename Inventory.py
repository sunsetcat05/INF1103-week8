import json

from physical_products import PhysicalProduct
from digital_products import DigitalProduct

DATA_FILE = "inventory.json"

# Maps the saved "type" identifier to the class that rebuilds it.
PRODUCT_TYPES = {
    PhysicalProduct.PRODUCT_TYPE: PhysicalProduct,
    DigitalProduct.PRODUCT_TYPE: DigitalProduct,
}


class Inventory:
    """Manages Product objects. It never looks inside them, it only calls
    their methods (display_information, to_dict, update_stock)."""

    def __init__(self):
        self._products = {}

    def add_product(self, product):
        """Return False if a product with this ID already exists."""
        if product.product_id in self._products:
            return False
        self._products[product.product_id] = product
        return True

    def find_product(self, product_id):
        return self._products.get(product_id)

    def display_all(self):
        if not self._products:
            print("Inventory is empty.")
            return
        for product in self._products.values():
            product.display_information()
            print()

    def update_stock(self, product_id, change):
        """Return False if the product is not found.
        Raises ValueError if the change would make stock negative."""
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(change)
        return True

    def search(self, keyword):
        keyword = keyword.lower()
        return [
            p
            for p in self._products.values()
            if keyword in p.name.lower() or keyword in p.product_id.lower()
        ]

    def save_to_file(self, filename=DATA_FILE):
        data = [product.to_dict() for product in self._products.values()]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, filename=DATA_FILE):
        """Replace the current contents with the saved inventory.
        Returns the number of products loaded."""
        with open(filename, "r", encoding="utf-8") as file:
            records = json.load(file)

        loaded = {}
        for record in records:
            product_class = PRODUCT_TYPES.get(record.get("type"))
            if product_class is None:
                print(f"Skipping record with unknown type: {record.get('type')!r}")
                continue
            product = product_class.from_dict(record)
            loaded[product.product_id] = product
        self._products = loaded
        return len(loaded)

    def __len__(self):
        return len(self._products)