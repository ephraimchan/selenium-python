from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Basic_test():
    driver = webdriver.Chrome()
    try:
        driver.get("https://google.com")
        # Add your test assertions here
        assert "Example" in driver.title
    finally:
        driver.close()
