"""
Page Object Model for OrangeHRM Admin Module - Add User
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time


class LoginPage(BasePage):
    """Page Object for Login Page"""

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    DASHBOARD_BREADCRUMB = (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")

    def login(self, username, password):
        """Login to OrangeHRM"""
        print(f">>> Attempting login with username: '{username}'")
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        self.wait_for_element_visible(self.DASHBOARD_BREADCRUMB)
        print("✅ Login successful, Dashboard loaded")


class AdminPage(BasePage):
    """Page Object for Admin Page - User Management"""

    # Navigation Locators
    ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    # Add User Form Locators
    USER_ROLE_DROPDOWN = (By.XPATH, "//label[text()='User Role']/parent::div/following-sibling::div//div[@class='oxd-select-text-input']")
    USER_ROLE_ESS = (By.XPATH, "//span[text()='ESS']")
    USER_ROLE_ADMIN = (By.XPATH, "//span[text()='Admin']")

    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/parent::div/following-sibling::div//input")
    EMPLOYEE_DROPDOWN_OPTION = (By.XPATH, "//div[@role='listbox']//span")

    STATUS_DROPDOWN = (By.XPATH, "//label[text()='Status']/parent::div/following-sibling::div//div[@class='oxd-select-text-input']")
    STATUS_ENABLED = (By.XPATH, "//span[text()='Enabled']")
    STATUS_DISABLED = (By.XPATH, "//span[text()='Disabled']")

    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//label[text()='Confirm Password']/parent::div/following-sibling::div//input")

    # Buttons
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[text()=' Cancel ']")

    # Success/Error Messages
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class,'oxd-toast-content')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

    # Search Locators
    SEARCH_USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")

    def is_admin_page(self):
        """Check if we're on Admin page"""
        print(">>> Checking if current page is Admin")
        try:
            result = self.is_element_present(self.ADMIN_MENU)
            print(f"✅ Is Admin page: {result}")
            return result
        except Exception as e:
            print(f"⚠️ Error checking Admin page: {e}")
            return False

    def navigate_to_admin(self):
        """Navigate to Admin menu"""
        print(">>> Navigating to Admin menu")
        try:
            self.click_element(self.ADMIN_MENU)
            time.sleep(2)
            print("✅ Admin menu clicked")
        except Exception as e:
            print(f"⚠️ Error navigating to Admin: {e}")
            raise

    def click_add_button(self):
        """Click Add button to open Add User form"""
        print(">>> Clicking Add button")
        try:
            self.click_element(self.ADD_BUTTON)
            time.sleep(2)
            print("✅ Add button clicked")
        except Exception as e:
            print(f"⚠️ Error clicking Add button: {e}")
            raise

    def select_user_role(self, role="ESS"):
        """Select user role from dropdown"""
        print(f">>> Selecting user role: {role}")
        try:
            self.click_element(self.USER_ROLE_DROPDOWN)
            time.sleep(1)

            if role.upper() == "ESS":
                self.click_element(self.USER_ROLE_ESS)
            else:
                self.click_element(self.USER_ROLE_ADMIN)

            print(f"✅ User Role selected: {role}")
        except Exception as e:
            print(f"⚠️ Error selecting user role: {e}")
            raise

    def select_employee_name(self, search_text="a"):
        """Select employee name from dropdown"""
        print(f">>> Selecting employee name with search: '{search_text}'")
        try:
            employee_field = self.wait.until(
                EC.presence_of_element_located(self.EMPLOYEE_NAME_INPUT)
            )
            employee_field.clear()
            employee_field.send_keys(search_text)
            time.sleep(2)

            dropdown_option = self.wait.until(
                EC.element_to_be_clickable(self.EMPLOYEE_DROPDOWN_OPTION)
            )
            dropdown_option.click()
            time.sleep(1)
            print("✅ Employee Name selected")
        except Exception as e:
            print(f"⚠️ Error selecting employee name: {e}")
            raise

    def select_status(self, status="Enabled"):
        """Select status from dropdown"""
        print(f">>> Selecting status: {status}")
        try:
            self.click_element(self.STATUS_DROPDOWN)
            time.sleep(1)

            if status == "Enabled":
                self.click_element(self.STATUS_ENABLED)
            else:
                self.click_element(self.STATUS_DISABLED)

            print(f"✅ Status selected: {status}")
        except Exception as e:
            print(f"⚠️ Error selecting status: {e}")
            raise

    def enter_username(self, username):
        print(f">>> Entering username: {username}")
        try:
            username_field = self.wait.until(
                EC.presence_of_element_located(self.USERNAME_INPUT)
            )
            username_field.clear()
            username_field.send_keys(username)
            print("✅ Username entered")
        except Exception as e:
            print(f"⚠️ Error entering username: {e}")
            raise

    def enter_password(self, password):
        print(f">>> Entering password")
        try:
            password_field = self.wait.until(
                EC.presence_of_element_located(self.PASSWORD_INPUT)
            )
            password_field.clear()
            password_field.send_keys(password)
            print("✅ Password entered")
        except Exception as e:
            print(f"⚠️ Error entering password: {e}")
            raise

    def enter_confirm_password(self, password):
        print(">>> Entering confirm password")
        try:
            confirm_password_field = self.wait.until(
                EC.presence_of_element_located(self.CONFIRM_PASSWORD_INPUT)
            )
            confirm_password_field.clear()
            confirm_password_field.send_keys(password)
            print("✅ Confirm Password entered")
        except Exception as e:
            print(f"⚠️ Error entering confirm password: {e}")
            raise

    def click_save(self):
        print(">>> Clicking Save button")
        try:
            self.click_element(self.SAVE_BUTTON)
            time.sleep(3)
            print("✅ Save button clicked")
        except Exception as e:
            print(f"⚠️ Error clicking Save button: {e}")
            raise

    def click_cancel(self):
        print(">>> Clicking Cancel button")
        try:
            self.click_element(self.CANCEL_BUTTON)
            print("✅ Cancel button clicked")
        except Exception as e:
            print(f"⚠️ Error clicking Cancel button: {e}")
            raise

    def get_success_message(self):
        print(">>> Retrieving success message")
        try:
            success_msg = self.wait.until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)
            )
            msg_text = success_msg.text
            print(f"📢 Success Message: {msg_text}")
            return msg_text
        except Exception:
            print("⚠️ No success message found")
            return None

    def get_error_messages(self):
        print(">>> Retrieving error messages")
        try:
            error_elements = self.find_elements(self.ERROR_MESSAGE)
            errors = [element.text for element in error_elements]
            print(f"📢 Error Messages: {errors}")
            return errors
        except Exception:
            print("⚠️ No error messages found")
            return []

    def search_user(self, username):
        print(f">>> Searching for user: {username}")
        try:
            search_field = self.wait.until(
                EC.presence_of_element_located(self.SEARCH_USERNAME_INPUT)
            )
            search_field.clear()
            search_field.send_keys(username)

            self.click_element(self.SEARCH_BUTTON)
            time.sleep(2)
            print(f"✅ Searched for user: {username}")
        except Exception as e:
            print(f"⚠️ Error searching user: {e}")
            raise

    def is_user_present_in_list(self, username):
        print(f">>> Checking if user '{username}' is present in list")
        try:
            user_locator = (By.XPATH, f"//div[text()='{username}']")
            result = self.is_element_present(user_locator)
            print(f"✅ User present: {result}")
            return result
        except Exception as e:
            print(f"⚠️ Error checking user presence: {e}")
            return False

    def is_user_saved_successfully(self):
        print(">>> Checking if user was saved successfully")
        try:
            success_msg = self.get_success_message()
            result = success_msg is not None and "Success" in success_msg
            print(f"✅ User saved successfully: {result}")
            return result
        except Exception as e:
            print(f"⚠️ Error checking if user saved: {e}")
            return False

    def fill_user_details(self, username, password, user_role="ESS", status="Enabled"):
        print(">>> Filling user details")
        try:
            self.select_user_role(user_role)
            self.select_employee_name()
            self.select_status(status)
            self.enter_username(username)
            self.enter_password(password)
            self.enter_confirm_password(password)
            print("✅ All user details filled")
        except Exception as e:
            print(f"⚠️ Error filling user details: {e}")
            raise

    def add_new_user(self, username, password, user_role="ESS", status="Enabled"):
        print(f">>> Adding new user: {username}")
        try:
            self.navigate_to_admin()
            self.click_add_button()
            self.fill_user_details(username, password, user_role, status)
            self.click_save()
            print(f"✅ User '{username}' creation process completed")
        except Exception as e:
            print(f"⚠️ Error in add_new_user flow: {e}")
            raise
