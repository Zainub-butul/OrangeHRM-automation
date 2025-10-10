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

    def test_add_employee_validation_errors(self, driver):
        print("\n>>> Test: Employee Validation Errors")
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        add_employee_page = AddEmployeePage(driver)

        login_page.login(Config.USERNAME, Config.PASSWORD)
        dashboard_page.navigate_to_pim()
        pim_page.navigate_to_add_employee()

        print(">>> Attempting to save employee without required fields")
        add_employee_page.save_employee()
        error_messages = add_employee_page.get_error_messages()
        assert len(error_messages) > 0, "⚠ Expected validation errors but none found"
        print(f"✅ Validation working - Found {len(error_messages)} error(s): {error_messages}")