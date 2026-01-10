from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.tests.system.selenium_driver import get_driver



def test_login_system():
    driver = get_driver()
    driver.get("http://127.0.0.1:5000/login")

    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 5).until(
        lambda d: "/feed" in d.current_url
    )

    assert "/feed" in driver.current_url