from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PIMPage(BasePage):
    # PIM Main Page Locators
    ADD_EMPLOYEE_MENU = (By.XPATH, "//a[text()='Add Employee']")
    EMPLOYEE_LIST_MENU = (By.XPATH, "//a[text()='Employee List']")
    PIM_BREADCRUMB = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb-module")

    def is_pim_page(self):
        """Check if we're on PIM page"""
        print(">>> Checking if current page is PIM")
        try:
            breadcrumb = self.get_text(self.PIM_BREADCRUMB)
            print(f">>> Breadcrumb text found: '{breadcrumb}'")
            is_pim = "PIM" in breadcrumb
            print(f"✅ Is PIM page: {is_pim}")
            return is_pim
        except Exception as e:
            print(f"⚠️ Error checking PIM page: {e}")
            return False

    def navigate_to_add_employee(self):
        """Navigate to Add Employee page"""
        print(">>> Navigating to Add Employee page")
        try:
            self.click_element(self.ADD_EMPLOYEE_MENU)
            print("✅ Clicked on Add Employee menu")
        except Exception as e:
            print(f"⚠️ Failed to navigate to Add Employee: {e}")
            raise

    def navigate_to_employee_list(self):
        """Navigate to Employee List page"""
        print(">>> Navigating to Employee List page")
        try:
            self.click_element(self.EMPLOYEE_LIST_MENU)
            print("✅ Clicked on Employee List menu")
        except Exception as e:
            print(f"⚠️ Failed to navigate to Employee List: {e}")
            raise
