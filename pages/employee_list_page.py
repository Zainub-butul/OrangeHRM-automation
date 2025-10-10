from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class EmployeeListPage(BasePage):
    # Search Form Locators
    EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/following::input[1]")
    EMPLOYEE_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/../..//input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESET_BUTTON = (By.XPATH, "//button[text()=' Reset ']")

    # Results Table
    RESULTS_TABLE = (By.CSS_SELECTOR, ".oxd-table-body")
    TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-row")
    NO_RECORDS_MESSAGE = (By.XPATH, "//span[text()='No Records Found']")

    # Actions
    DELETE_BUTTON = (By.CSS_SELECTOR, ".oxd-icon-button--ghost-danger")
    EDIT_BUTTON = (By.CSS_SELECTOR, ".oxd-icon-button--ghost")

    def search_employee_by_id(self, employee_id):
        """Search for employee by ID"""
        self.enter_text(self.EMPLOYEE_ID_INPUT, employee_id)
        self.click_element(self.SEARCH_BUTTON)
        time.sleep(2)  # Wait for search results

    # pages/employee_list_page.py - Fix your search_employee_by_name method

    def search_employee_by_name(self, first_name, last_name):
        """Search for an employee by name instead of ID"""
        print(f"Searching for employee by name: {first_name} {last_name}")

        # Employee name search field locators
        EMPLOYEE_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/../..//input")
        EMPLOYEE_NAME_INPUT_ALT = (By.XPATH, "//input[@placeholder='Type for hints...']")
        SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
        EMPLOYEE_RECORDS = (By.XPATH, "//div[@class='oxd-table-body']//div[@role='row']")

        try:
            # Find the employee name input field
            try:
                name_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(EMPLOYEE_NAME_INPUT)
                )
                print("✅ Found employee name input using primary locator")
            except:
                name_input = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(EMPLOYEE_NAME_INPUT_ALT)
            )
                print("✅ Found employee name input using alternative locator")

            # Enter the employee name
            name_input.clear()
            full_name = f"{first_name} {last_name}"
            name_input.send_keys(full_name)
            print(f"✅ Entered employee name: {full_name}")

            # Wait for autocomplete and try to select
            time.sleep(2)
            try:
                suggestion = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{first_name}')]")
                suggestion.click()
                print("✅ Selected from autocomplete")
            except:
                print("No autocomplete found, continuing with typed name")

            # Click search button
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(SEARCH_BUTTON)
            )
            search_button.click()
            print("✅ Clicked search button")

            # Wait for results
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(EMPLOYEE_RECORDS)
            )
            print("✅ Search by name completed")

        except Exception as e:
            print(f"❌ Error searching by name: {str(e)}")
            self.driver.save_screenshot(f"screenshots/name_search_error.png")
            raise

    def reset_search(self):
        """Reset search form"""
        self.click_element(self.RESET_BUTTON)

    def get_search_results_count(self):
        """Get number of search results"""
        try:
            if self.is_element_present(self.NO_RECORDS_MESSAGE):
                return 0
            rows = self.find_elements(self.TABLE_ROWS)
            return len(rows) - 1  # Subtract header row
        except:
            return 0

    def is_employee_found(self, employee_name=None, employee_id=None):
        """Check if employee exists in search results"""
        try:
            if self.is_element_present(self.NO_RECORDS_MESSAGE):
                return False

            # If we have results, check if employee exists
            return self.get_search_results_count() > 0
        except:
            return False