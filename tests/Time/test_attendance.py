# tests/test_attendance.py
import pytest
import datetime
from pages.dashboard_page import DashboardPage
from pages.attendance_page import AttendancePage
from pages.login_page import LoginPage  # Replace with your actual login page object

@pytest.mark.usefixtures("driver")
class TestAttendance:

    def test_punch_in_out_and_view_records(self, driver):
        print(">>> Test: Attendance Punch In/Out and View Records started")

        # ---------- Login ----------
        print(">>> Logging in with Admin credentials")
        login_page = LoginPage(driver)
        login_page.login(username="Admin", password="admin123")  # replace with valid creds
        print("✅ Login successful")

        # ---------- Dashboard ----------
        print(">>> Navigating to Time module from Dashboard")
        dashboard = DashboardPage(driver)
        dashboard.navigate_to_time()
        print("✅ Navigation to Time module successful")

        # ---------- Attendance ----------
        attendance = AttendancePage(driver)

        # Punch In
        print(">>> Punching In")
        punch_in_success = attendance.punch_in(note="Starting work for the day")
        assert punch_in_success, "⚠️ Punch In failed"
        print("✅ Punch In successful")

        # Punch Out
        print(">>> Punching Out")
        punch_out_success = attendance.punch_out(note="Work finished for the day")
        assert punch_out_success, "⚠️ Punch Out failed"
        print("✅ Punch Out successful")

        # Navigate to My Records
        print(">>> Navigating to My Records")
        attendance.navigate_to_my_records()
        print("➡️ Navigated to My Records")

        # Filter records by today's date
        today = datetime.date.today().strftime("%Y-%m-%d")
        print(f">>> Filtering records by today's date: {today}")
        filter_success = attendance.filter_records_by_date(today)
        assert filter_success, "⚠️ Failed to filter records by date"
        print("✅ Records filtered for today")

        # Verify records exist
        print(">>> Retrieving attendance records")
        records = attendance.get_records()
        assert len(records) > 0, "⚠️ No records found"
        print(f"✅ Records found: {len(records)}")

        # Verify total work duration is displayed
        print(">>> Checking total work duration")
        total_duration = attendance.get_total_duration()
        assert total_duration is not None, "⚠️ Total duration not displayed"
        print(f"✅ Total Work Duration: {total_duration}")

        print(">>> Test: Attendance Punch In/Out and View Records finished")
