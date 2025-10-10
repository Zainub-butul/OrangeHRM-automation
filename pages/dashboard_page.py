from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from utils.logger import get_logger    # ✅ Import logger

class DashboardPage(BasePage):
    # Initialize logger
    log = get_logger(__name__)

    # Locators
    HEADER = (By.XPATH, "//h6[text()='Dashboard']")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_OPTION = (By.LINK_TEXT, "Logout")
    QUICK_LAUNCH_CARDS = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div[2]/div/div[1]')
    EMPLOYEE_GRAPH = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[6]')
    PROFILE_NAME = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[3]/ul/li/span/p')

    ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    LEAVE_MENU = (By.XPATH, "//span[text()='Leave']")
    TIME_MENU = (By.XPATH, "//span[text()='Time']")

    def __init__(self, driver):
        super().__init__(driver)
        self.log.info("DashboardPage initialized")

    # Actions
    def is_dashboard_displayed(self):
        visible = len(self.driver.find_elements(*self.HEADER)) > 0
        self.log.info(f"Dashboard displayed: {visible}")
        return visible

    def get_quick_launch_items(self):
        elements = self.find_elements(self.QUICK_LAUNCH_CARDS)
        items = [el.text.strip() for el in elements if el.text.strip()]
        self.log.info(f"Quick launch items found: {items}")
        return items

    def wait_for_element_and_return(self, locator):
        self.log.debug(f"Waiting for element: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def is_graph_displayed(self):
        try:
            graph_element = self.wait_for_element_and_return(self.EMPLOYEE_GRAPH)
            displayed = graph_element.is_displayed()
            self.log.info("Employee graph is displayed")
            return displayed
        except:
            self.log.warning("Employee graph not displayed")
            return False

    def get_profile_name(self):
        element = self.wait.until(EC.visibility_of_element_located(self.PROFILE_NAME))
        name = element.text.strip()
        self.log.info(f"Profile name: {name}")
        return name

    def open_profile_menu(self):
        self.log.info("Opening profile menu")
        self.click_element(self.PROFILE_NAME)

    def is_logout_option_available(self):
        self.open_profile_menu()
        available = self.is_element_present(self.LOGOUT_OPTION)
        self.log.info(f"Logout option available: {available}")
        return available

    # Navigation
    def navigate_to_admin(self):
        self.log.info("Navigating to Admin page")
        self.click(self.ADMIN_MENU)

    def navigate_to_pim(self):
        self.log.info("Navigating to PIM page")
        self.click(self.PIM_MENU)

    def navigate_to_leave(self):
        self.log.info("Navigating to Leave page")
        self.click(self.LEAVE_MENU)

    def navigate_to_time(self):
        self.log.info("Navigating to Time page")
        self.click(self.TIME_MENU)

    def logout(self):
        self.log.info("Logging out from the application")
        self.open_profile_menu()
        self.click(self.LOGOUT_OPTION)
