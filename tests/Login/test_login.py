import pytest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger  # ✅ import logger

# ------------------ Logger ------------------
log = get_logger(__name__)

# ------------------ Test Data ------------------
test_data = [
    ("Admin", "admin123", "valid"),        # correct login
    ("Admin", "wrongPass", "invalid"),     # wrong password
    ("wrongUser", "admin123", "invalid"),  # wrong username
    ("", "admin123", "invalid"),           # empty username
    ("Admin", "", "invalid"),              # empty password
]

# ------------------ Test Function ------------------
@pytest.mark.parametrize("username,password,expected", test_data)
def test_login(driver, username, password, expected):
    """
    Login test for different scenarios.
    Uses LoginPage POM with driver fixture from conftest.py
    """
    log.info(f"===== START: test_login with username='{username}' and password='{password}' =====")

    login_page = LoginPage(driver)

    # Perform login
    log.info(f"Performing login with username='{username}' and password='{password}'")
    login_page.login(username, password)

    if expected == "valid":
        log.info("Expecting a successful login")
        # Wait for dashboard header to appear
        dashboard_header = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )
        assert dashboard_header.is_displayed(), "❌ Dashboard header not found"
        assert "dashboard" in driver.current_url.lower(), "❌ URL does not contain 'dashboard'"
        log.info("✅ Login successful, Dashboard header displayed and URL verified")
    else:
        log.info("Expecting login to fail")
        # Try to capture error message
        error_message = login_page.get_error_message()
        if error_message:
            log.warning(f"Login failed as expected with error message: '{error_message}'")
            assert error_message == "Invalid credentials", f"❌ Unexpected error message: {error_message}"
        else:
            # Check required field messages
            required_fields = driver.find_elements(By.CSS_SELECTOR, ".oxd-input-group__message")
            assert any("Required" in field.text for field in required_fields), "❌ No required field message displayed"
            log.info("✅ Login failed as expected, required field message displayed")

    log.info(f"===== END: test_login with username='{username}' =====\n")
