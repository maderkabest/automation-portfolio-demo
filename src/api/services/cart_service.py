"""Cart service for products."""

from src.api.client import APIClient


class CartService:
    def __init__(self, client: APIClient):
        self.client = client

    def add_item(self, cart_id, product_id, quantity, token):
        response = self.client.post(
            f"/carts/{cart_id}",
            json={"product_id": product_id, "quantity": quantity},
            headers={"Authorization": f"Bearer {token}"},
        )
        return response

    def create(self, token):
        return self.client.post("/carts", json=None, headers={"Authorization": f"Bearer {token}"})
