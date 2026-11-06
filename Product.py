from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class holding everything common to every product.
    It cannot be instantiated because get_fulfilment_info() is abstract."""

    def __init__(self, product_id, name, price, stock_quantity):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        # Single underscore: "protected", so subclasses may use them
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock_quantity = stock_quantity

    # Read-only access (encapsulation)
    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def stock_quantity(self):
        return self._stock_quantity

    def update_stock(self, change):
        """Add (positive) or remove (negative) stock."""
        if self._stock_quantity + change < 0:
            raise ValueError(
                f"Not enough stock: only {self._stock_quantity} available."
            )
        self._stock_quantity += change

    def display_information(self):
        print(f"[{self._product_id}] {self._name}")
        print(f"  Price: ${self._price:.2f}")
        print(f"  Stock: {self._stock_quantity}")

    def to_dict(self):
        """Common data only - subclasses extend this."""
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock_quantity": self._stock_quantity,
        }
    def to_report_dict(self):
        """Saved fields plus computed information, for exported reports."""
        data = self.to_dict()
        data["fulfilment_info"] = self.get_fulfilment_info()
        return data

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message describing how this product is fulfilled."""
        pass