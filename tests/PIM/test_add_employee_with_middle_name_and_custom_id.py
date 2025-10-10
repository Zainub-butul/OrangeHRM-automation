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

    def test_add_employee_with_middle_name_and_custom_id(self, driver):
        print("\n>>> Test: Add Employee with Middle Name and Custom ID")
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        add_employee_page = AddEmployeePage(driver)

        # Login and navigate
        login_page.login(Config.USERNAME, Config.PASSWORD)
        print("✅ Logged in")
        dashboard_page.navigate_to_pim()
        pim_page.navigate_to_add_employee()

        # Fill details
        first_name, middle_name, last_name = "John", "Michael", "Doe"
        print(f">>> Filling employee details: {first_name} {middle_name} {last_name}")
        add_employee_page.fill_employee_details_with_middle_name(first_name, middle_name, last_name)

        # Capture auto-generated ID
        employee_id = add_employee_page.get_employee_id()
        print(f">>> Auto-generated Employee ID: {employee_id}")

        # Save employee
        add_employee_page.save_employee()
        assert add_employee_page.is_employee_saved_successfully(), "⚠ Employee was not saved successfully"
        print(f"✅ Employee created: {first_name} {middle_name} {last_name} (ID: {employee_id})")