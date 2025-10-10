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

    def test_search_created_employee(self, driver):
        print("\n>>> Test: Search for Created Employee")
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        pim_page = PIMPage(driver)
        add_employee_page = AddEmployeePage(driver)
        employee_list_page = EmployeeListPage(driver)

        login_page.login(Config.USERNAME, Config.PASSWORD)
        dashboard_page.navigate_to_pim()
        pim_page.navigate_to_add_employee()

        first_name, last_name = "SearchTest", "Employee"
        print(f">>> Creating employee for search test: {first_name} {last_name}")
        add_employee_page.fill_basic_employee_details(first_name, last_name)
        employee_id = add_employee_page.get_employee_id()
        add_employee_page.save_employee()

        pim_page.navigate_to_employee_list()
        employee_list_page.search_employee_by_name(first_name, last_name)

        assert employee_list_page.is_employee_found(), f"⚠ Employee with ID {employee_id} not found"
        print(f"✅ Employee found in search: {first_name} {last_name} (ID: {employee_id})")