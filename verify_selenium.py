import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Initializing Chrome Driver...")

# 1. Set up Chrome options
options = webdriver.ChromeOptions()
# For local testing, we leave headless mode OFF so you can see it work!
# options.add_argument("--headless") 

# 2. Automatically download and manage the driver executable
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    print("Opening browser and navigating to Google...")
    driver.get("https://www.google.com")
    
    # Let it sit for 3 seconds so you can visually see it open
    time.sleep(3) 
    
    # Get the title of the page
    page_title = driver.title
    print(f"Success! Successfully connected. Page Title is: '{page_title}'")

except Exception as e:
    print(f"Something went wrong: {e}")

finally:
    print("Closing browser...")
    driver.quit()