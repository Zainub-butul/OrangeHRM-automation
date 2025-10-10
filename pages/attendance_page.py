from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


class AttendancePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # default wait

        # ---------- Menu locators ----------
        self.attendance_menu = (By.XPATH, "//span[contains(text(),'Attendance')]")
        self.punch_in_out_option = (By.XPATH, "//a[contains(text(),'Punch In/Out')]")
        self.my_records_option = (By.XPATH, "//a[text()='My Records']")

        # ---------- Punch In/Out locators ----------
        self.punch_note = (By.XPATH, "//textarea[contains(@class,'oxd-textarea')]")
        self.punch_button = (By.XPATH, "//button[contains(@class,'orangehrm-attendance-card-action') or contains(@class,'oxd-button')]")
        self.toast_message = (By.CLASS_NAME, "oxd-toast-content")

        # ---------- My Records locators ----------
        self.date_input = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div[2]/form/div[1]/div/div/div/div[2]/div/div/input')
        self.view_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div[2]/form/div[2]/button')
        self.records_rows = (By.XPATH, "//div[@class='oxd-table-body']/div")
        self.total_duration = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[2]/div[1]/span')

    # ---------- Navigation ----------
    def open_attendance_dropdown(self):
        print(">>> Opening Attendance menu")
        loader = (By.CSS_SELECTOR, ".oxd-loading-spinner")
        self.wait.until(EC.invisibility_of_element_located(loader))
        menu = self.wait.until(EC.element_to_be_clickable(self.attendance_menu))
        print(">>> Attendance menu clickable, attempting click")
        self.safe_click(menu)
        print("✅ Attendance menu opened")

    def navigate_to_punch_in_out(self):
        print(">>> Navigating to Punch In/Out page")
        self.open_attendance_dropdown()
        option = self.wait.until(EC.element_to_be_clickable(self.punch_in_out_option))
        self.safe_click(option)
        print("✅ Punch In/Out page opened")

    def navigate_to_my_records(self):
        print(">>> Navigating to My Records page")
        self.open_attendance_dropdown()
        option = self.wait.until(EC.element_to_be_clickable(self.my_records_option))
        self.safe_click(option)
        print("✅ My Records page opened")

    # ---------- Punch In/Out ----------
    def punch_in(self, note=""):
        print(">>> Performing Punch In")
        return self._punch_action(note, action="in")

    def punch_out(self, note=""):
        print(">>> Performing Punch Out")
        return self._punch_action(note, action="out")

    def _punch_action(self, note="", action="in"):
        """Generic punch in/out action with toast check."""
        self.navigate_to_punch_in_out()

        # Enter note if provided
        if note:
            note_field = self.wait.until(EC.presence_of_element_located(self.punch_note))
            note_field.clear()
            note_field.send_keys(note)
            print(f">>> Note entered for Punch {action.capitalize()}: {note}")

        # Click punch button
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.punch_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            print(f">>> Clicking Punch {action.capitalize()} button")
            self.safe_click(button)
            print(f"✅ Punch {action.capitalize()} button clicked")
        except TimeoutException:
            print(f"⚠️ Punch {action.capitalize()} button not found or not clickable")
            return False

        # Wait for toast message
        try:
            toast = self.wait.until(EC.visibility_of_element_located(self.toast_message))
            msg = toast.text
            print(f"📢 Punch {action.capitalize()} Toast Message: {msg}")
            return "Successfully" in msg or "Overlapping" in msg
        except TimeoutException:
            print(f"⚠️ No toast found after Punch {action.capitalize()}")
            return False

    # ---------- My Records ----------
    def filter_records_by_date(self, date_str):
        print(f">>> Filtering attendance records for date: {date_str}")
        try:
            loader = (By.CSS_SELECTOR, ".oxd-loading-spinner")
            WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located(loader))

            date_input = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.date_input)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", date_input)
            self.driver.execute_script("arguments[0].value = arguments[1];", date_input, date_str)
            print(f">>> Date entered: {date_str}")

            view_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.view_button)
            )
            self.driver.execute_script("arguments[0].click();", view_btn)
            print(f"✅ Filter applied and View button clicked for date {date_str}")
            return True
        except TimeoutException:
            print("⚠️ Could not find Date Input or View button")
            return False

    def get_records(self):
        records = self.driver.find_elements(*self.records_rows)
        print(f"📄 Total records found: {len(records)}")
        return records

    def get_total_duration(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.total_duration))
            total = element.text.strip()
            print(f"⏱️ Total Work Duration: {total}")
            return total
        except TimeoutException:
            print("⚠️ Total Duration element not found")
            return None

    # ---------- Utility ----------
    def safe_click(self, element):
        """Click element safely with JS or ActionChains fallback."""
        try:
            element.click()
            print("✅ Element clicked successfully")
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)
            print("✅ Element clicked via JS due to intercept")
        except Exception:
            ActionChains(self.driver).move_to_element(element).click().perform()
            print("✅ Element clicked via ActionChains fallback")
