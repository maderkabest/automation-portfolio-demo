"""Authentication service for user registration and login."""

from src.api.client import APIClient
from src.models.user import UserRegister, UserLogin


class AuthService:
    def __init__(self, client: APIClient):
        self.client = client

    def register(self, user: UserRegister):
        payload = user.model_dump()
        address = payload.pop("address")
        flat = {**payload, **{f"address[{k}]": v for k, v in address.items()}}
        return self.client.post("/users/register", data=flat)

    def login(self, user: UserLogin):
        return self.client.post("/users/login", data=user.model_dump())
