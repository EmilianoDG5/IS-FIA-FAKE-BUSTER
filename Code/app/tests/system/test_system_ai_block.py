from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.tests.system.selenium_driver import get_driver


def test_system_ai_block_popup():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    try:
        
        driver.get("http://127.0.0.1:5000/login")

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.TAG_NAME, "button").click()

        wait.until(EC.url_contains("/feed"))

        driver.get("http://127.0.0.1:5000/new_post")

        wait.until(EC.presence_of_element_located((By.NAME, "titolo")))
        driver.find_element(By.NAME, "titolo").send_keys(
            "No Change Expected for ESPN Political Agenda Despite Huge Subscriber Decline - Breitbart"
        )
        driver.find_element(By.NAME, "testo").send_keys(
            "As more and more sports fans turn off ESPN to protest the network’s social and political agenda, p...."
        )

        driver.find_element(By.TAG_NAME, "button").click()

        # 🔹 resta su new_post
        wait.until(EC.url_contains("/new_post"))

        # 🔹 il popup DEVE esistere nel DOM
        popup = driver.find_element(By.ID, "appelloPopup")
        assert popup is not None

    finally:
        driver.quit()


