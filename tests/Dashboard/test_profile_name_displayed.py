import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.dashboard_page import DashboardPage
from config import Config
from utils.logger import get_logger   # ✅ Import the logger


# ✅ Create logger instance for this test module
log = get_logger(__name__)


# ------------------ FIXED FIXTURE ------------------
@pytest.fixture(scope="function")
def login_valid():
    """
    Opens the website and logs in directly using valid credentials.
    Each test gets a fresh browser session.
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    log.info("🚀 Starting browser for login fixture...")

    # Setup Chrome
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    log.info(f"🌍 Navigating to URL: {Config.BASE_URL}")
    driver.get(Config.BASE_URL)

    # Login
    log.info("🔑 Entering login credentials...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    ).send_keys("Admin")

    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    log.info("⏳ Waiting for Dashboard page to load...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
    )
    log.info("✅ Successfully logged in and Dashboard loaded.")

    yield driver

    log.info("🛑 Closing browser after test execution.")
    driver.quit()


# ------------------ TEST CASE ------------------

def test_profile_name_displayed(login_valid):
    log.info("===== START: test_profile_name_displayed =====")
    driver = login_valid
    dashboard = DashboardPage(driver)

    profile_name = dashboard.get_profile_name()
    log.info(f"🔎 Profile name displayed: {profile_name}")

    assert profile_name.strip() != "", "❌ Profile name is not displayed"

    log.info("✅ Profile name validated successfully.")
    log.info("===== END: test_profile_name_displayed =====\n")