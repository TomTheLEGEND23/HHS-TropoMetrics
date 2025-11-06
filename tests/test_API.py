import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


lijst_zonder_error = []
lijst_met_error = []
lijst_tijden = []
teller = 0 
aantal = 5
# Configure Chrome to run headless. Options are created once and reused for each iteration.
options = webdriver.ChromeOptions()
# Use the modern headless mode where available. Fallback to legacy --headless if needed.
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
# Common flags that help in headless / CI environments
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
while teller <= aantal:
    teller += 1
    tijd_start = time.time()
    driver.get("http://10.0.0.101:30081/api?api_key='demo'")
    
    try:    
        WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'geef water') or contains(text(), 'Water geven is nu niet nodig')]")))
        
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_zonder_error.append(tijd_verschil)
        print("Succesvolle poging ", teller)    
    except: 
        tijd_eind = time.time()
        tijd_verschil = tijd_eind - tijd_start
        lijst_met_error.append(tijd_verschil)
        print("Mislukte poging ", teller)
driver.quit()
        
average = sum (lijst_zonder_error) / len(lijst_zonder_error)
print("Latency succesvolle aanvragen: ", str(average) + "s")


