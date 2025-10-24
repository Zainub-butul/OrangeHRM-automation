class Config:
    # OrangeHRM Demo URL
    BASE_URL = "https://opensource-demo.orangehrmlive.com/"

    # Default credentials for demo
    USERNAME = "Admin"
    PASSWORD = "admin123"

    # Browser settings
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    IMPLICIT_WAIT = 15
    EXPLICIT_WAIT = 30

    # Screenshot settings
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_PATH = "screenshots/"


