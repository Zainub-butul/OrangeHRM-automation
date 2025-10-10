import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.add_employee_page import AddEmployeePage
from config import Config
from utils.helpers import TestDataGenerator


@pytest.fixture
def login_valid(driver):
    """Login fixture"""
    driver.get(Config.BASE_URL)
    login_page = LoginPage(driver)
    login_page.login(Config.USERNAME, Config.PASSWORD)
    yield


@pytest.fixture
def add_employee_page_fixture(driver, login_valid):
    """Navigate to Add Employee page and provide AddEmployeePage"""
    dashboard_page = DashboardPage(driver)
    pim_page = PIMPage(driver)
    add_employee_page = AddEmployeePage(driver)

    # Navigate to Add Employee
    dashboard_page.navigate_to_pim()
    pim_page.navigate_to_add_employee()
    yield add_employee_page


def test_auto_generated_employee_id(add_employee_page_fixture):
    """Test: Verify auto-generated Employee ID"""
    add_employee_page = add_employee_page_fixture

    # Generate random first and last names
    first_name = TestDataGenerator.generate_random_string(6)
    last_name = TestDataGenerator.generate_random_string(6)

    # Fill basic details
    add_employee_page.fill_basic_employee_details(first_name, last_name)

    # Get auto-generated Employee ID
    employee_id = add_employee_page.get_employee_id()
    assert employee_id, "⚠ Employee ID was not generated!"
    print(f"✅ Auto-generated Employee ID: {employee_id}")
