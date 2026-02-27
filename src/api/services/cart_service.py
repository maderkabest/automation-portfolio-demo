"""Cart service for products."""

from src.api.client import APIClient

class CartService:
    def __init__(self, client: APIClient):
        self.client = client

    def add_item(self, cart_id, product_id, quantity):
        response = self.client.post(
            f"/carts/{cart_id}",
            json={"product_id": product_id, "quantity": quantity}
            )
    return response
