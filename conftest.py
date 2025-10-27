import pytest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import Config


# -------------------------
# LOGGING SETUP
# -------------------------
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logging.info("===== Test Session Started =====")


# -------------------------
# DRIVER SETUP
# -------------------------
@pytest.fixture(scope="session")
def driver_setup():
    """Setup WebDriver based on configuration"""
    logging.info(f"Initializing WebDriver for browser: {Config.BROWSER}")

    # Detect if running in GitHub Actions
    is_github = os.getenv("GITHUB_ACTIONS") == "true"

    if Config.BROWSER.lower() == "chrome":
        options = Options()

        # Disable Chrome password popups
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)

        # ✅ Headless in GitHub, normal in local
        if is_github or Config.HEADLESS:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)  # ✅ Fixed line

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Chrome WebDriver launched successfully.")

    elif Config.BROWSER.lower() == "firefox":
        options = FirefoxOptions()
        if is_github or Config.HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        logging.info("Firefox WebDriver launched successfully.")

    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(40)
    try:
        driver.maximize_window()
    except Exception:
        logging.warning("Unable to maximize window (headless mode).")

    yield driver

    driver.quit()
    logging.info("Driver closed after session.")


# -------------------------
# PER-TEST FIXTURE
# -------------------------
@pytest.fixture(scope="function")
def driver(driver_setup):
    """Provide fresh driver session for each test"""
    logging.info(f"Opening base URL: {Config.BASE_URL}")
    driver_setup.get(Config.BASE_URL)
    yield driver_setup

    logging.info("Clearing cookies and storage after test.")
    driver_setup.delete_all_cookies()
    driver_setup.execute_script("window.localStorage.clear();")
    driver_setup.execute_script("window.sessionStorage.clear();")


# -------------------------
# CAPTURE SCREENSHOTS ON FAILURE
# -------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed and Config.SCREENSHOT_ON_FAILURE:
        driver = item.funcargs.get('driver')
        if driver:
            os.makedirs(Config.SCREENSHOT_PATH, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(Config.SCREENSHOT_PATH, screenshot_name)
            driver.save_screenshot(screenshot_path)
            logging.error(f"Test FAILED: {item.name}. Screenshot saved at {screenshot_path}")
            print(f"Screenshot saved: {screenshot_path}")
        else:
            logging.error(f"Test FAILED: {item.name}. No driver available to capture screenshot.")
