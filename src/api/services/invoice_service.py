"""Invoice service for products."""

from src.api.client import APIClient


class InvoiceService:
    def __init__(self, client: APIClient):
        self.client = client

    def get_all(self, token):
        return self.client.get("/invoices", headers={"Authorization": f"Bearer {token}"})
