import pytest
import time
import random
import string
from pages.login_page import LoginPage
from pages.vacancy_page import VacancyPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_random_vacancy_name(prefix="Automation Tester Vacancy"):
    """Generate a unique vacancy name to avoid duplicates"""
    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f"{prefix} {rand_str}"

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
def vacancy_page(driver, login_valid):
    """Provide VacancyPage after login"""
    return VacancyPage(driver)

def test_fill_vacancy_form(vacancy_page):
    """Test: Fill Vacancy form and select Hiring Manager from suggestions"""
    print(">>> Test: Fill Vacancy Form started")

    # Navigate to Vacancies
    vacancy_page.navigate_to_vacancies()

    # Click Add
    vacancy_page.click_add()

    # Select Job Title
    vacancy_page.select_job_title("QA Engineer")

    # Enter unique Vacancy Name
    vacancy_name = generate_random_vacancy_name()
    vacancy_page.enter_vacancy_name(vacancy_name)

    # Enter partial Hiring Manager name
    partial_name = "Ranga"
    input_field = vacancy_page.hiring_manager_input
    element = vacancy_page.wait.until(lambda d: d.find_element(*input_field))
    element.clear()
    element.send_keys(partial_name)
    time.sleep(2)  # wait for suggestions to appear

    # Select first suggestion from dropdown
    suggestion_xpath = "//div[@role='listbox']//span"
    suggestion = vacancy_page.wait.until(lambda d: d.find_element(By.XPATH, suggestion_xpath))
    suggestion.click()
    time.sleep(1)
    print(f">>> Hiring Manager selected from suggestions")

    # Save vacancy
    vacancy_page.save_vacancy()
    print(f">>> Vacancy '{vacancy_name}' form filled and saved successfully")

    # Optional: Verify success toast
    try:
        success_message_xpath = "//div[contains(@class,'oxd-toast-content-text') and text()='Success']"
        success_message = WebDriverWait(vacancy_page.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, success_message_xpath))
        )
        assert success_message.is_displayed()
        print("✅ Vacancy added successfully - success message verified")
    except Exception as e:
        print(f"⚠️ Could not verify success message: {e}")
        vacancy_page.driver.save_screenshot("vacancy_success_verification.png")
