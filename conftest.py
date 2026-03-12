"""Global pytest fixtures shared across all test modules."""

import os
import allure
import pytest
import psycopg2

from faker import Faker
from playwright.sync_api import sync_playwright
from src.api.services.auth_service import AuthService
from src.models.user import UserRegister, Address
from src.api.client import APIClient
from dotenv import load_dotenv

load_dotenv()
fake = Faker("en_US")
base_url = os.getenv("BASE_URL")
ui_url = os.getenv("UI_URL")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


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


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.set_default_timeout(60000)
        yield page
        context.tracing.stop(path="test-results/trace.zip")
        browser.close()


@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_database, user=db_user, password=db_password)
    yield conn
    conn.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to Allure report on test failure for UI tests."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("browser")
        if page is not None:
            screenshot = page.screenshot()
            allure.attach(screenshot, name="screenshot on failure", attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="session", autouse=True)
def allure_env_setup(request):
    """Automatically generates the Environment block for the Allure report."""
    yield
    allure_dir = request.config.getoption("--alluredir", default=None)
    if allure_dir:
        env_file = os.path.join(allure_dir, "environment.properties")
        with open(env_file, "w") as f:
            f.write("OS=Windows\n")
            f.write("Browser=Chromium (Playwright)\n")
            f.write(f"API_URL={os.getenv('BASE_URL', base_url)}\n")
            f.write(f"UI_URL={os.getenv('UI_URL', ui_url)}\n")
