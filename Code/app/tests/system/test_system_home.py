from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.tests.system.selenium_driver import get_driver



def test_home_page():
    driver = get_driver()
    driver.get("http://127.0.0.1:5000/")
    assert "FakeBuster" in driver.page_source
    driver.quit()