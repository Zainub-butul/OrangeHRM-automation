from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import time


class AddEmployeePage(BasePage):
    # Add Employee Form Locators
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMPLOYEE_ID_INPUT = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/input')  # Second input field
    PROFILE_PICTURE = (By.CSS_SELECTOR, "input[type='file']")

    # Create Login Details Section
    CREATE_LOGIN_TOGGLE = (By.CSS_SELECTOR, ".oxd-switch-input")
    USERNAME_INPUT = (By.XPATH, "//label[text()='Username']/following::input[1]")
    STATUS_ENABLED_RADIO = (By.XPATH, "//span[text()='Enabled']/preceding-sibling::input[@type='radio']")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Password']/following::input[1]")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//label[text()='Confirm Password']/following::input[1]")

    # Buttons
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[text()=' Cancel ']")

    # Success/Error Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".oxd-toast-content-text")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

    # Status dropdown options
    STATUS_ENABLED = (By.XPATH, "//span[text()='Enabled']")
    STATUS_DISABLED = (By.XPATH, "//span[text()='Disabled']")

    def is_add_employee_page(self):
        """Check if we're on Add Employee page"""
        print(">>> Checking if Add Employee page is loaded")
        try:
            result = self.is_element_present(self.FIRST_NAME_INPUT)
            print(f"✅ Add Employee page loaded: {result}")
            return result
        except Exception as e:
            print(f"⚠ Error checking Add Employee page: {e}")
            return False

    def fill_basic_employee_details(self, first_name, last_name):
        """Fill basic employee details and wait for auto-generated employee ID"""
        try:
            print(f">>> Filling First Name: {first_name}")
            first_name_field = self.wait.until(EC.presence_of_element_located(self.FIRST_NAME_INPUT))
            first_name_field.clear()
            first_name_field.send_keys(first_name)

            print(f">>> Filling Last Name: {last_name}")
            last_name_field = self.wait.until(EC.presence_of_element_located(self.LAST_NAME_INPUT))
            last_name_field.clear()
            last_name_field.send_keys(last_name)

            # Tab to trigger ID generation
            last_name_field.send_keys(Keys.TAB)
            print(">>> Waiting for Employee ID to auto-generate")
            time.sleep(3)

            emp_id = self.get_employee_id()
            print(f"✅ Auto-generated Employee ID: {emp_id}")
        except Exception as e:
            print(f"⚠ Error filling basic employee details: {e}")
            raise



    def get_employee_id(self, retries=5, delay=0.5):
        for _ in range(retries):
            element = self.find_element(self.EMPLOYEE_ID_INPUT)
            emp_id = element.get_attribute("value")
            if emp_id:
                print(f">>> Retrieved Employee ID: {emp_id}")
                return emp_id
            time.sleep(delay)
        print("⚠ Could not get Employee ID after retries")
        return None


    def enable_create_login_details(self):
        """Enable the create login details toggle switch"""
        try:
            print(">>> Enabling Create Login Details toggle")
            time.sleep(3)
            toggle = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.CREATE_LOGIN_TOGGLE)
            )

            is_enabled = (
                    toggle.is_selected() or
                    toggle.get_attribute('checked') == 'true' or
                    toggle.get_attribute('aria-checked') == 'true'
            )

            if not is_enabled:
                try:
                    toggle.click()
                    print("✅ Toggle clicked")
                except:
                    self.driver.execute_script("arguments[0].click();", toggle)
                    print("✅ Toggle clicked via JS")

            time.sleep(3)
            return True
        except Exception as e:
            print(f"⚠ Toggle error: {e}")
            raise

    def fill_login_details(self, username, password, status="Enabled"):
        """Fill login details section"""
        print(f">>> Filling login details: username={username}, status={status}")
        self.enable_create_login_details()

        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, password)
        print("✅ Login credentials entered")

        if status != "Enabled":
            try:
                status_radio = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[text()='{status}']/preceding-sibling::input[@type='radio']"))
                )
                status_radio.click()
                print(f"✅ Status set to: {status}")
            except TimeoutException:
                try:
                    status_label = self.driver.find_element(By.XPATH, f"//span[text()='{status}']")
                    status_label.click()
                    print(f"✅ Status label clicked for: {status}")
                except:
                    print(f"⚠ Could not set status to '{status}', using default")

    def upload_profile_picture(self, file_path):
        """Upload profile picture"""
        try:
            print(f">>> Uploading profile picture: {file_path}")
            file_input = self.find_element(self.PROFILE_PICTURE)
            file_input.send_keys(file_path)
            print("✅ Profile picture uploaded")
            return True
        except Exception as e:
            print(f"⚠ Could not upload profile picture: {e}")
            return False

    def save_employee(self):
        """Click Save button"""
        print(">>> Clicking Save button")
        self.click_element(self.SAVE_BUTTON)
        time.sleep(2)
        print("✅ Employee saved")

    def cancel_employee_creation(self):
        """Click Cancel button"""
        print(">>> Clicking Cancel button")
        self.click_element(self.CANCEL_BUTTON)
        print("✅ Employee creation canceled")

    def get_success_message(self):
        """Get success message text"""
        try:
            msg = self.get_text(self.SUCCESS_MESSAGE)
            print(f">>> Success message: {msg}")
            return msg
        except:
            print("⚠ No success message found")
            return None

    def get_error_messages(self):
        """Get all error messages"""
        try:
            error_elements = self.find_elements(self.ERROR_MESSAGE)
            errors = [element.text for element in error_elements]
            print(f">>> Error messages: {errors}")
            return errors
        except:
            print("⚠ Could not retrieve error messages")
            return []

    def is_employee_saved_successfully(self, timeout=10):
        """Check if employee was saved successfully"""
        try:
            success_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE)  # locator for toast
            )
            success_msg = success_element.text
            print(f">>> Success message text: {success_msg}")
            return "Success" in success_msg
        except Exception as e:
            print(f"⚠ Error verifying employee save: {e}")
            return False

    def fill_middle_name(self, middle_name):
        """Fill the middle name field separately"""
        try:
            print(f">>> Filling Middle Name: {middle_name}")
            middle_name_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "middleName"))
            )
            middle_name_field.clear()
            middle_name_field.send_keys(middle_name)
            print(f"✅ Middle name filled: {middle_name}")
        except Exception as e:
            print(f"⚠ Error filling middle name: {str(e)}")
            raise

    def fill_employee_details_with_middle_name(self, first_name, middle_name, last_name, employee_id=None):
        print(f">>> Filling employee details: {first_name} {middle_name} {last_name}")
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.MIDDLE_NAME_INPUT).send_keys(middle_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

        if employee_id:
            emp_id_field = self.driver.find_element(*self.EMPLOYEE_ID_INPUT)
            emp_id_field.clear()
            emp_id_field.send_keys(employee_id)
            print(f">>> Employee ID set: {employee_id}")

        self.driver.find_element(*self.SAVE_BUTTON).click()
        print("✅ Employee details submitted")
