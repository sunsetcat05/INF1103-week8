from Product import Product


class DigitalProduct(Product):
    """Inherits from Product only. It is NOT CanBeShipped."""

    PRODUCT_TYPE = "digital"

    def __init__(self, product_id, name, price, stock_quantity, download_size):
        super().__init__(product_id, name, price, stock_quantity)
        if download_size <= 0:
            raise ValueError("Download size must be greater than 0.")
        self._download_size = download_size

    @property
    def download_size(self):
        return self._download_size

    def display_information(self):
        super().display_information()
        print(f"  Download size: {self._download_size:.2f} MB")

    def get_fulfilment_info(self):
        return (
            f"'{self._name}' is a digital product delivered by "
            f"download ({self._download_size:.2f} MB)."
        )

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self._download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock_quantity"],
            data["download_size"],
        )