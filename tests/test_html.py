import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Get base URL and API key from environment variables or use defaults
BASE_URL = os.environ.get("TEST_BASE_URL", "http://10.0.0.101:30081")
API_KEY = os.environ.get("TEST_API_KEY", "test")

# Build URL with or without API key parameter
if API_KEY:
    TEST_URL = f"{BASE_URL}/index.html?api_key={API_KEY}"
else:
    TEST_URL = f"{BASE_URL}/index.html"

lijst_zonder_error = []
lijst_met_error = []
lijst_tijden = []
teller = 0 
aantal = 2000

# Configure Chrome to run headless. Options are created once and reused for each iteration.
options = webdriver.ChromeOptions()
# Use the modern headless mode where available. Fallback to legacy --headless if needed.
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
# Common flags that help in headless / CI environments
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
# Disable caching to ensure fresh requests
options.add_argument("--disk-cache-size=0")
options.add_argument("--disable-application-cache")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Set page load timeout
options.page_load_strategy = 'normal'

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

print(f"Testing HTML page: {TEST_URL}")
print(f"Number of requests: {aantal}")
print("-" * 60)

while teller < aantal:
    teller += 1
    tijd_start = time.time()
    
    try:
        # Clear cookies and cache between iterations
        driver.delete_all_cookies()
        
        driver.get(TEST_URL)
        
        # Wait for page to be fully loaded
        WebDriverWait(driver, 5).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # Wait for expected content to appear (case-insensitive)
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'geef water') or contains(text(), 'Water geven is nu niet nodig')]"))
        )
        
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_zonder_error.append(tijd_verschil)
        print(f"✓ Request {teller}: Success - {tijd_verschil:.3f}s")
        
    except Exception as e:
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_met_error.append(tijd_verschil)
        print(f"✗ Request {teller}: Failed - {tijd_verschil:.3f}s - Error: {str(e)}")

driver.quit()

# Print summary
print("\n" + "=" * 60)
print("HTML Test Summary")
print("=" * 60)
print(f"Total requests: {aantal}")
print(f"Successful: {len(lijst_zonder_error)}")
print(f"Failed: {len(lijst_met_error)}")
print(f"Success rate: {(len(lijst_zonder_error)/aantal)*100:.1f}%")


df = pd.DataFrame(lijst_zonder_error, columns=["data"])
df.to_csv('resultatenHTML.csv', index=False)

if lijst_zonder_error:
    average = sum(lijst_zonder_error) / len(lijst_zonder_error)
    min_time = min(lijst_zonder_error)
    max_time = max(lijst_zonder_error)
    print(f"\nLatency Statistics (Successful requests):")
    print(f"  Average: {average:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")
else:
    print("\nNo successful requests to calculate latency.")

if lijst_met_error:
    print(f"\nFailed requests average time: {sum(lijst_met_error)/len(lijst_met_error):.3f}s")
    print(f"Failed requests min time: {min(lijst_met_error):.3f}s")

print("=" * 60)

# Exit with error code if any requests failed
if lijst_met_error:
    sys.exit(1)
else:
    sys.exit(0)