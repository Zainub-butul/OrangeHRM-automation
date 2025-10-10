from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger  # ✅ Import logger

class LoginPage(BasePage):
    """Page Object for Login Page"""

    # Initialize logger
    log = get_logger(__name__)

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, ".orangehrm-login-forgot-header")

    def __init__(self, driver):
        """Initialize with WebDriver from conftest.py"""
        super().__init__(driver)
        self.log.info("LoginPage initialized")

    def login(self, username: str, password: str):
        """Perform login with given credentials"""
        self.log.info(f"Attempting login with username: '{username}'")
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        self.log.info("Login button clicked")

    def get_error_message(self) -> str | None:
        """Return error message text if present, else None"""
        if self.is_element_present(self.ERROR_MESSAGE):
            msg = self.get_text(self.ERROR_MESSAGE)
            self.log.warning(f"Login error message displayed: {msg}")
            return msg
        self.log.info("No login error message displayed")
        return None

    def is_login_page(self) -> bool:
        """Check if login button is present to confirm login page"""
        present = self.is_element_present(self.LOGIN_BUTTON)
        self.log.info(f"Is login page displayed: {present}")
        return present

    def click_forgot_password(self):
        """Click forgot password link"""
        if self.is_element_present(self.FORGOT_PASSWORD_LINK):
            self.click_element(self.FORGOT_PASSWORD_LINK)
            self.log.info("Clicked 'Forgot Password' link")
        else:
            self.log.error("Forgot Password link not found on Login Page")
            raise Exception("Forgot Password link not found on Login Page")
