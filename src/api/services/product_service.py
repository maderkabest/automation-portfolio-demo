"""Product service for retrieving products."""

from src.api.client import APIClient


class ProductService:
    def __init__(self, client: APIClient):
        self.client = client

    def get_all(self):
        return self.client.get("/products")
