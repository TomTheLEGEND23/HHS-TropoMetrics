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
while teller <= aantal:
    teller += 1
    driver = webdriver.Chrome()
    tijd_start = time.time()

    driver.get("http://10.0.0.101:30081/")
    
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
print("Gemiddelde tijd zonder error: ", average)


