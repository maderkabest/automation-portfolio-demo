"""Authentication service for user registration and login."""

from src.api.client import APIClient
from src.models.user import UserRegister, UserLogin

class AuthService:
    def __init__(self, client: APIClient):
        self.client = client

    def register(self, user: UserRegister):
        return self.client.post("/users/register", json=user.model_dump())

    def login(self, user: UserLogin):
        return self.client.post("/users/login", json=user.model_dump())
