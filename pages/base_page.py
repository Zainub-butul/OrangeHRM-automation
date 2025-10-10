from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config import Config  # Fixed import
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def find_element(self, locator):
        """Find a single element"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Find multiple elements"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        """Click an element"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def enter_text(self, locator, text):
        """Enter text into an input field"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        """Get text from an element"""
        element = self.find_element(locator)
        return element.text

    def wait_for_element_visible(self, locator):
        """Wait for element to be visible"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator):
        """Wait for element to be clickable"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    def get_page_title(self):
        """Get current page title"""
        return self.driver.title

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    # Add these methods to your existing BasePage class

    def safe_click(self, element):
        """Safely click an element using multiple strategies"""
        try:
            # Try regular click first
            element.click()
        except ElementClickInterceptedException:
            # If intercepted, try JavaScript click
            self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            # As last resort, try ActionChains
            ActionChains(self.driver).move_to_element(element).click().perform()

    def wait_for_element_clickable_with_timeout(self, locator, timeout):
        """Wait for element to be clickable with custom timeout"""
        custom_wait = WebDriverWait(self.driver, timeout)
        return custom_wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_visible_with_timeout(self, locator, timeout):
        """Wait for element to be visible with custom timeout"""
        custom_wait = WebDriverWait(self.driver, timeout)
        return custom_wait.until(EC.visibility_of_element_located(locator))

    def enter_text_with_return_status(self, locator, text):
        """Enter text into an input field and return success status"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            print(f"Error entering text: {e}")
            return False

    def click(self, locator):
        """Alias for click_element to simplify page methods"""
        return self.click_element(locator)

























