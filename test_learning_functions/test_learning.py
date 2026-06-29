import pytest
import os
from selenium import webdriver
import selenium.webdriver.chrome.options as Options
from selenium.webdriver.support.ui import WebDriverWait



options = Options.Options()

driver = webdriver.Chrome(options=options)
driver.get("https://practicetestautomation.com/practice-test-login/")



wait = WebDriverWait(driver, 10)


driver.find_element("id", "username").send_keys("student")
driver.find_element("id", "password").send_keys("Password123")  


element = wait.until(lambda d: d.find_element("id", "submit"))
element.click()
