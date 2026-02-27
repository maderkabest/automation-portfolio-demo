"""Pydantic models for API request and response validation."""

from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    address: Address
    phone: str
    dob: str
    password: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
