from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_full_flow():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/login")

    driver.find_element(By.NAME, "username").send_keys("user")
    driver.find_element(By.NAME, "password").send_keys("password")
    driver.find_element(By.TAG_NAME, "button").click()

    driver.get("http://127.0.0.1:5000/new_post")

    driver.find_element(By.NAME, "titolo").send_keys("Test News")
    driver.find_element(By.NAME, "testo").send_keys(
        "This is a realistic news article with sufficient content."
    )

    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)

    driver.quit()
