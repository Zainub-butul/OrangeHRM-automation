import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Ensure root path is in sys.path for module import resolution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importing application-specific modules
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.add_employee_page import AddEmployeePage
from config import Config
from utils.helpers import TestDataGenerator


# -----------------------------
# Fixture: fresh driver per test
# -----------------------------
@pytest.fixture
def fresh_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(Config.BASE_URL)  # Open login page
    yield driver
    driver.quit()


# -----------------------------
# Test Class
# -----------------------------
class TestEmployeeAddition:

    @pytest.mark.parametrize("first_name,last_name,has_middle_name", [
        ("Alice", "Johnson", False),
        ("Bob", "Smith", True),
        ("Carol", "Davis", False),
        ("David", "Wilson", True),
        ("Emma", "Brown", False)
    ])
    def test_add_multiple_employees_with_different_data(self, fresh_driver, first_name, last_name, has_middle_name):
        driver = fresh_driver  # Use fresh browser session

        print(f"\n>>> Test: Add Employee - {first_name} {last_name}")

        # Initialize page objects
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        add_employee_page = AddEmployeePage(driver)

        # Step 1: Login
        login_page.login(Config.USERNAME, Config.PASSWORD)

        # Step 2: Navigate to Add Employee
        dashboard_page.navigate_to_pim()
        pim_page.navigate_to_add_employee()

        # Step 3: Fill Employee Data
        middle_name = TestDataGenerator.generate_random_string(6) if has_middle_name else ""
        print(f">>> Creating employee: {first_name} {middle_name} {last_name}")

        add_employee_page.fill_basic_employee_details(first_name, last_name)
        if middle_name:
            add_employee_page.fill_middle_name(middle_name)

        # Step 4: Save Employee
        employee_id = add_employee_page.get_employee_id()
        add_employee_page.save_employee()

        # Step 5: Assert employee was created
        assert add_employee_page.is_employee_saved_successfully(), f"❌ Failed to create employee: {first_name} {last_name}"
        print(f"✅ Employee created successfully: {first_name} {middle_name} {last_name} (ID: {employee_id})")

        # Step 6: Prepare for next iteration (navigate again to Add Employee page)
        # Not strictly needed since each test has fresh driver, but safe:
        pim_page.navigate_to_add_employee()
