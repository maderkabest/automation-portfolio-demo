"""API tests for user authentication endpoints."""

import os
import pytest

from faker import Faker
from src.api.services.auth_service import AuthService
from src.api.client import APIClient
from src.models.user import UserRegister, Address, UserLogin
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("BASE_URL")
fake = Faker("en_US")


@pytest.fixture
def enter_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.numerify(text="0########")
    dob = fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat()
    password = fake.password(length=12, digits=True, upper_case=True)
    email = fake.email()
    street = fake.street_address()
    city = fake.city()
    state = fake.state()
    country = fake.country()
    postal_code = fake.postcode()

    address = Address(street=street, city=city, state=state, country=country, postal_code=postal_code)

    user = UserRegister(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        dob=dob,
        password=password,
        email=email,
    )

    auth = AuthService(APIClient(base_url))
    response = auth.register(user)
    return user, response


def test_register_returns_201(enter_user):
    user, response = enter_user
    assert response.status_code == 201


def test_login_returns_token(enter_user):
    user, _ = enter_user
    user = UserLogin(email=user.email, password=user.password)
    auth = AuthService(APIClient(base_url))
    response = auth.login(user)
    data = response.json()
    assert "access_token" in data
