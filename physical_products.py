from Product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """Single inheritance from Product, plus the CanBeShipped interface."""

    PRODUCT_TYPE = "physical"
    BASE_SHIPPING_FEE = 5.00   # flat fee in dollars
    RATE_PER_KG = 2.00         # extra dollars per kilogram

    def __init__(self, product_id, name, price, stock_quantity, weight):
        super().__init__(product_id, name, price, stock_quantity)
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    # Overrides Product.display_information, reusing the parent's output
    def display_information(self):
        super().display_information()
        print(f"  Weight: {self._weight:.2f} kg")

    # Implements the abstract method from Product
    def get_fulfilment_info(self):
        return (
            f"'{self._name}' is a physical product and requires "
            f"shipping ({self._weight:.2f} kg)."
        )

    # Implements the abstract method from CanBeShipped
    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_FEE + self.RATE_PER_KG * self._weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self._weight
        return data
    
    def to_report_dict(self):
        data = super().to_report_dict()
        data["shipping_cost"] = self.calculate_shipping_cost()
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock_quantity"],
            data["weight"],
        )