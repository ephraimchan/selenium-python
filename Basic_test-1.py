from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def Basic_test():
    # Selenium Grid Hub URL (change to your grid hub address)
    grid_url = os.getenv('SELENIUM_HUB_URL', 'http://localhost:4444')
    
    # Define desired capabilities
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Connect to Selenium Grid
    driver = webdriver.Remote(
        command_executor=f'{grid_url}/wd/hub',
        options=options
    )
    
    try:
        driver.get("https://google.com")
        # Wait for page title to load
        WebDriverWait(driver, 10).until(
            EC.title_contains("Google")
        )
        # Add your test assertions here
        assert "Google" in driver.title
        print("✓ Test passed: Google page loaded successfully")
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    Basic_test()

