from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class VacancyPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.admin_tab = (By.XPATH, "//span[text()='Admin']")
        self.recruitment_tab = (By.XPATH, "//span[text()='Recruitment']")
        self.vacancies_menu = (By.XPATH, "//a[contains(.,'Vacancies')]")

        self.add_button = (By.XPATH, "//button[normalize-space()='Add']")
        self.job_title_dropdown = (By.XPATH, "//label[text()='Job Title']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
        self.vacancy_name_input = (By.XPATH, "//label[text()='Vacancy Name']/../following-sibling::div/input")
        self.hiring_manager_input = (By.XPATH, "//label[text()='Hiring Manager']/../following-sibling::div//input")
        self.save_button = (By.XPATH, "//button[normalize-space()='Save']")

    # Actions
    def navigate_to_vacancies(self):
        try:
            print(">>> Navigating to Recruitment tab")
            recruitment = self.wait.until(EC.element_to_be_clickable(self.recruitment_tab))
            recruitment.click()
            print(">>> Recruitment tab clicked")

            print(">>> Waiting for Vacancies menu")
            vacancies = self.wait.until(EC.element_to_be_clickable(self.vacancies_menu))
            vacancies.click()
            print(">>> Vacancies menu clicked successfully")
        except Exception as e:
            print(f"!!! Error in navigate_to_vacancies: {e}")
            self.driver.save_screenshot("navigate_to_vacancies_error.png")
            raise

    def click_add(self):
        try:
            print(">>> Clicking Add button")
            self.wait.until(EC.element_to_be_clickable(self.add_button)).click()
            print(">>> Add button clicked successfully")
        except Exception as e:
            print(f"!!! Error in click_add: {e}")
            self.driver.save_screenshot("click_add_error.png")
            raise

    def select_job_title(self, title_text):
        try:
            print(f">>> Selecting Job Title: {title_text}")
            dropdown = self.wait.until(EC.element_to_be_clickable(self.job_title_dropdown))
            dropdown.click()
            print(">>> Dropdown clicked")

            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@role='option']//span[text()='{title_text}']"))
            )
            option.click()
            print(f">>> Job Title '{title_text}' selected successfully")
        except Exception as e:
            print(f"!!! Error in select_job_title: {e}")
            self.driver.save_screenshot("select_job_title_error.png")
            raise

    def enter_vacancy_name(self, name):
        try:
            print(f">>> Entering Vacancy Name: {name}")
            self.wait.until(EC.visibility_of_element_located(self.vacancy_name_input)).send_keys(name)
            print(">>> Vacancy Name entered successfully")
        except Exception as e:
            print(f"!!! Error in enter_vacancy_name: {e}")
            self.driver.save_screenshot("enter_vacancy_name_error.png")
            raise

    def enter_hiring_manager(self, manager_name):
        try:
            print(f">>> Entering Hiring Manager: {manager_name}")
            self.wait.until(EC.visibility_of_element_located(self.hiring_manager_input)).send_keys(manager_name)
            print(">>> Hiring Manager entered successfully")
        except Exception as e:
            print(f"!!! Error in enter_hiring_manager: {e}")
            self.driver.save_screenshot("enter_hiring_manager_error.png")
            raise

    def save_vacancy(self):
        try:
            print(">>> Clicking Save button")
            self.wait.until(EC.element_to_be_clickable(self.save_button)).click()
            print(">>> Save button clicked successfully")
        except Exception as e:
            print(f"!!! Error in save_vacancy: {e}")
            self.driver.save_screenshot("save_vacancy_error.png")
            raise
