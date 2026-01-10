from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.tests.system.selenium_driver import get_driver



def test_system_create_post():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://127.0.0.1:5000/login")

        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.TAG_NAME, "button").click()

        # aspetta che il login sia completato
        wait.until(EC.url_contains("/feed"))

        driver.get("http://127.0.0.1:5000/new_post")

        # ⬇️ QUESTA È LA CHIAVE
        titolo = wait.until(
            EC.presence_of_element_located((By.NAME, "titolo"))
        )

        titolo.send_keys("Post reale")
        driver.find_element(By.NAME, "testo").send_keys(
            "This is a valid news article with enough content"
        )

        driver.find_element(By.TAG_NAME, "button").click()

        wait.until(EC.url_contains("/my_posts"))
        assert "/my_posts" in driver.current_url

    finally:
        driver.quit()
