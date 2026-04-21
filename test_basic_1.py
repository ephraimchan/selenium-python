import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import Login_Parameter
import time

# 1. Use a fixture for WebDriver setup
@pytest.fixture
def driver_options():
    options = Options()
    # options.add_argument('--headless') # Keep commented to see in NoVNC
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options

# 2. Use parametrize to loop through your 10 scenarios
@pytest.mark.parametrize("scenario", Login_Parameter.LOGIN_SCENARIOS)
def test_login_scenarios(scenario, driver_options):
    grid_url = os.getenv('SELENIUM_HUB_URL', 'http://selenium-hub:4444')
    
    # Initialize WebDriver
    driver = webdriver.Remote(
        command_executor=f'{grid_url}/wd/hub',
        options=driver_options
    )
    
    try:
        print(f"Running: {scenario['desc']}")
        driver.get("https://the-internet.herokuapp.com/login")
        
        wait = WebDriverWait(driver, 10)
        
        # Interactions
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(scenario['username'])
        driver.find_element(By.ID, "password").send_keys(scenario['password'])
        driver.find_element(By.CSS_SELECTOR, "button.radius").click()

        # Validation
        message_element = wait.until(EC.presence_of_element_located((By.ID, "flash")))
        actual_text = message_element.text

        if scenario['expected'] == "success":
            assert "You logged into a secure area!" in actual_text
        else:
            assert "is invalid" in actual_text or "Your username is invalid!" in actual_text
            
        # Keep window open for NoVNC visibility
        time.sleep(5) 

    finally:
        driver.quit()