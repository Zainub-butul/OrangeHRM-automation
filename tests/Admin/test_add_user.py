"""
Test Case for OrangeHRM Admin Module - Add User
"""

import pytest
import time
from pages.admin_page import AdminPage
from pages.login_page import LoginPage


@pytest.fixture
def login_valid(driver):
    """Log in before running tests"""
    print(">>> Opening OrangeHRM demo site")
    driver.get("https://opensource-demo.orangehrmlive.com/")
    login_page = LoginPage(driver)
    print(">>> Logging in with Admin credentials")
    login_page.login("Admin", "admin123")
    print("✅ Login completed")
    yield


@pytest.fixture
def admin_page(driver, login_valid):
    """Provide AdminPage after login"""
    print(">>> Initializing AdminPage fixture")
    page = AdminPage(driver)
    print("✅ AdminPage fixture ready")
    return page


def test_add_user(admin_page):
    """Test adding a new user with valid data"""
    print(">>> Test: Add User started")

    # Navigate to Admin module
    print(">>> Navigating to Admin module")
    admin_page.navigate_to_admin()

    print(">>> Clicking Add button")
    admin_page.click_add_button()

    # Generate unique username
    unique_username = f"testuser_{int(time.time())}"
    password = "Test@123"
    print(f">>> Generated unique username: {unique_username}")

    # Fill form
    print(">>> Selecting User Role: ESS")
    admin_page.select_user_role("ESS")

    print(">>> Selecting Employee Name: John Doe")
    admin_page.select_employee_name("John Doe")  # searches and selects first employee

    print(">>> Selecting Status: Enabled")
    admin_page.select_status("Enabled")

    print(f">>> Entering Username: {unique_username}")
    admin_page.enter_username(unique_username)

    print(">>> Entering Password")
    admin_page.enter_password(password)

    print(">>> Entering Confirm Password")
    admin_page.enter_confirm_password(password)

    print(">>> Clicking Save")
    admin_page.click_save()

    # Assert user added - check success message
    print(">>> Verifying if user was saved successfully")
    assert admin_page.is_user_saved_successfully(), "⚠️ User was not saved successfully"
    print(f"✅ User '{unique_username}' saved successfully")

    # Verify user appears in list
    print(f">>> Searching for user in list: {unique_username}")
    time.sleep(2)
    admin_page.search_user(unique_username)
    assert admin_page.is_user_present_in_list(unique_username), f"⚠️ User '{unique_username}' not found in list"
    print(f"✅ User '{unique_username}' found in list")
    print(">>> Test: Add User completed successfully")
