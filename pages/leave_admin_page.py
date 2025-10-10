import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LeaveAdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        logger.info("LeaveAdminPage initialized.")

    # Locators
    LEAVE_MENU = (By.XPATH, "//span[text()='Leave']")
    CONFIGURE_MENU = (By.XPATH, "//span[text()='Configure ']")
    LEAVE_TYPES = (By.LINK_TEXT, "Leave Types")
    ADD_BUTTON = (By.XPATH, "//button[text()=' Add ']")
    LEAVE_TYPE_NAME = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div/div[2]/input')

    SAVE_BUTTON = (By.XPATH, "//button[text()=' Save ']")
    SUCCESS_TOAST = (By.CSS_SELECTOR, ".oxd-toast-content")

    # Entitlement Locators
    ENTITLEMENTS_MENU = (By.XPATH, "//span[text()='Entitlements ']")
    ADD_ENTITLEMENTS = (By.LINK_TEXT, "Add Entitlements")
    EMPLOYEE_FIELD = (By.XPATH, "//input[@placeholder='Type for hints...']")
    EMPLOYEE_OPTION = (By.XPATH, "//div[@role='listbox']//span")  # First match
    LEAVE_TYPE_DROPDOWN = (By.XPATH, "//label[text()='Leave Type']/following::div[@class='oxd-select-wrapper'][1]")
    LEAVE_TYPE_OPTION = lambda self, leave_type: (By.XPATH, f"//span[text()='{leave_type}']")
    ENTITLEMENT_DAYS = (By.XPATH, "//label[text()='Entitlement']/following::input[1]")
    SAVE_ENTITLEMENT = (By.XPATH, "//button[text()=' Save ']")
    CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Confirm']")

    # ---------------- Methods ----------------
    def navigate_to_leave_types(self):
        logger.info("Navigating to Leave Types page...")
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_MENU)).click()
        logger.info("Clicked Leave menu.")
        self.wait.until(EC.element_to_be_clickable(self.CONFIGURE_MENU)).click()
        logger.info("Clicked Configure menu.")
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_TYPES)).click()
        logger.info("Clicked Leave Types.")

    def add_leave_type(self, leave_name):
        logger.info(f"Adding new leave type: {leave_name}")
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).click()
        logger.info("Clicked Add button.")

        # Wait for popup to appear
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Add Leave Type']")))
        logger.info("Add Leave Type popup appeared.")

        name_input = self.wait.until(EC.visibility_of_element_located(self.LEAVE_TYPE_NAME))
        name_input.clear()
        logger.info("Cleared leave type name input.")
        name_input.send_keys(leave_name)
        logger.info(f"Entered leave type name: {leave_name}")

        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()
        logger.info("Clicked Save button for leave type.")

        toast_text = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_TOAST)).text
        logger.info(f"Leave type added successfully. Toast message: '{toast_text}'")
        return toast_text

    def add_entitlement(self, employee_name, leave_type, days):
        logger.info(f"Adding entitlement for employee '{employee_name}', leave type '{leave_type}', days '{days}'")
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_MENU)).click()
        logger.info("Clicked Leave menu.")
        self.wait.until(EC.element_to_be_clickable(self.ENTITLEMENTS_MENU)).click()
        logger.info("Clicked Entitlements menu.")
        self.wait.until(EC.element_to_be_clickable(self.ADD_ENTITLEMENTS)).click()
        logger.info("Clicked Add Entitlements.")

        # Enter employee
        emp_input = self.wait.until(EC.visibility_of_element_located(self.EMPLOYEE_FIELD))
        emp_input.clear()
        emp_input.send_keys(employee_name)
        logger.info(f"Entered employee name: {employee_name}")
        self.wait.until(EC.element_to_be_clickable(self.EMPLOYEE_OPTION)).click()
        logger.info("Selected employee from suggestions.")

        # Select leave type
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_TYPE_DROPDOWN)).click()
        logger.info("Clicked Leave Type dropdown.")
        self.wait.until(EC.element_to_be_clickable(self.LEAVE_TYPE_OPTION(leave_type))).click()
        logger.info(f"Selected leave type: {leave_type}")

        # Enter entitlement days
        self.wait.until(EC.visibility_of_element_located(self.ENTITLEMENT_DAYS)).send_keys(str(days))
        logger.info(f"Entered entitlement days: {days}")

        self.wait.until(EC.element_to_be_clickable(self.SAVE_ENTITLEMENT)).click()
        logger.info("Clicked Save button for entitlement.")

        # Handle confirmation modal
        modal = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'oxd-dialog-container')]"))
        )
        logger.info("Confirmation modal appeared.")

        confirm_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.CONFIRM_BUTTON)
        )
        confirm_btn.click()
        logger.info("Clicked Confirm button on modal.")

        # Wait for success toast
        toast_text = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.SUCCESS_TOAST)
        ).text
        logger.info(f"Entitlement added successfully. Toast message: '{toast_text}'")
        return toast_text
