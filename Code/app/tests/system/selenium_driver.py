from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()

    options.add_argument("--incognito")
    options.add_argument("--user-data-dir=/tmp/selenium-profile")

    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "password_manager_enabled": False,
        "safebrowsing.enabled": False
    })

    options.add_argument("--disable-features=PasswordLeakDetection")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-save-password-bubble")

    return webdriver.Chrome(options=options)
