import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.add_employee_page import AddEmployeePage
from pages.employee_list_page import EmployeeListPage
from config import Config
from utils.helpers import TestDataGenerator
import time
from selenium.webdriver.support.ui import WebDriverWait

class TestEmployeeAddition:

    def test_add_employee_with_login_credentials(self, driver):
        print("\n>>> Test: Add Employee with Login Credentials")
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        add_employee_page = AddEmployeePage(driver)

        login_page.login(Config.USERNAME, Config.PASSWORD)
        dashboard_page.navigate_to_pim()
        pim_page.navigate_to_add_employee()

        first_name = TestDataGenerator.generate_random_string(6)
        last_name = TestDataGenerator.generate_random_string(8)
        username = f"user_{TestDataGenerator.generate_random_string(5)}"
        password = "TestPass123!"
        print(f">>> Employee details: {first_name} {last_name}, username: {username}")

        add_employee_page.fill_basic_employee_details(first_name, last_name)
        add_employee_page.fill_login_details(username, password, "Enabled")
        employee_id = add_employee_page.get_employee_id()
        add_employee_page.save_employee()

        assert add_employee_page.is_employee_saved_successfully(), "⚠ Employee was not saved successfully"
        print(f"✅ Employee with login created: {first_name} {last_name} (Username: {username}, ID: {employee_id})")