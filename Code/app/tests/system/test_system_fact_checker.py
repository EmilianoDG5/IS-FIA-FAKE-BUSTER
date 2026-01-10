from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.tests.system.selenium_driver import get_driver



def test_system_fact_checker_publish_appello():
    driver = get_driver()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("http://127.0.0.1:5000/login")

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys("factchecker")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.TAG_NAME, "button").click()

        wait.until(EC.url_contains("/dashboard"))

        assert "Fact Checker" in driver.page_source

        # Pubblica appello
        publish_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//form[contains(@action,'publish')]//button"))
        )
        publish_btn.click()

        wait.until(EC.url_contains("/dashboard"))

    finally:
        driver.quit()
