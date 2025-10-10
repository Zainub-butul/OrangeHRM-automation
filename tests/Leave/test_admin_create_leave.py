import pytest
import logging
from pages.login_page import LoginPage
from pages.leave_admin_page import LeaveAdminPage
from config import Config

# Configure logger for tests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("driver")
class TestAdminLeave:

    def test_create_leave_type_and_assign_entitlement(self, driver):
        login = LoginPage(driver)
        leave_admin = LeaveAdminPage(driver)

        # Step 1: Login as Admin
        logger.info("Starting test: Create Leave Type and Assign Entitlement")
        logger.info(f"Logging in as Admin: {Config.USERNAME}")
        login.login(Config.USERNAME, Config.PASSWORD)
        logger.info("Login successful.")

        # Step 2: Navigate & Add Leave Type
        logger.info("Navigating to Leave Types page.")
        leave_admin.navigate_to_leave_types()
        logger.info("Adding new leave type: 'happy Leave'")
        toast_message = leave_admin.add_leave_type("happy Leave")
        logger.info(f"Leave type creation toast message: '{toast_message}'")
        assert "Successfully Saved" in toast_message or "successfully" in toast_message.lower()
        logger.info("Leave type added successfully.")

        # Step 3: Assign Entitlement to Employee
        logger.info("Assigning entitlement to employee 'John A doe'.")
        entitlement_msg = leave_admin.add_entitlement("John A Doe", "happy Leave", 10)
        logger.info(f"Entitlement assignment toast message: '{entitlement_msg}'")
        assert "Successfully Saved" in entitlement_msg or "successfully" in entitlement_msg.lower()
        logger.info("Entitlement assigned successfully.")
        logger.info("Test completed successfully.")
