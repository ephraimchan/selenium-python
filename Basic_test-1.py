from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

def Basic_test():
    # Use the service name defined in your docker-compose or the Grid IP
    grid_url = os.getenv('SELENIUM_HUB_URL', 'http://host.docker.internal:4444')
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print(f"Connecting to Selenium Grid at: {grid_url}")
    
    try:
        # Connect to Selenium Grid
        driver = webdriver.Remote(
            command_executor=f'{grid_url}/wd/hub',
            options=options
        )
        
        driver.get("https://google.com")
        
        # Wait for page title to load
        WebDriverWait(driver, 10).until(
            EC.title_contains("Google")
        )
        
        assert "Google" in driver.title
        print("✓ Test passed: Google page loaded successfully")
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        raise # This ensures Jenkins sees the stage as 'FAILED'
    finally:
        # Always quit to free up the slot on the Grid
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    Basic_test()