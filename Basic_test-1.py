from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import Login_Parameter  # Importing your scenarios

def run_login_test(scenario, grid_url, options):
    print(f"Running Scenario: {scenario['desc']}...")
    
    driver = None
    try:
        driver = webdriver.Remote(
            command_executor=f'{grid_url}/wd/hub',
            options=options
        )
        
        driver.get("https://the-internet.herokuapp.com/login")
        
        # Locators
        username_field = (By.ID, "username")
        password_field = (By.ID, "password")
        login_button = (By.CSS_SELECTOR, "button.radius")
        flash_message = (By.ID, "flash")

        # Interaction
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(username_field)).send_keys(scenario['username'])
        driver.find_element(*password_field).send_keys(scenario['password'])
        driver.find_element(*login_button).click()

        # Validation
        message_element = wait.until(EC.presence_of_element_located(flash_message))
        actual_text = message_element.text

        if scenario['expected'] == "success":
            assert "You logged into a secure area!" in actual_text
        else:
            assert "is invalid" in actual_text or "Your username is invalid!" in actual_text

        print(f"  ✓ {scenario['desc']} passed.")

    except Exception as e:
        print(f"  ✗ {scenario['desc']} failed: {str(e)}")
        raise e
    finally:
        if driver:
            driver.quit()

def main():
    grid_url = os.getenv('SELENIUM_HUB_URL', 'http://localhost:4444')
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Loop through all 10 scenarios
    for scenario in Login_Parameter.LOGIN_SCENARIOS:
        try:
            run_login_test(scenario, grid_url, options)
        except Exception:
            continue # Continue to next test even if one fails

if __name__ == "__main__":
    main()