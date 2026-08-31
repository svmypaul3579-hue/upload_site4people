import logs
# pyrefly: ignore [missing-import]
from selenium import webdriver
# pyrefly: ignore [missing-import]
from selenium.webdriver.common.by import By
# pyrefly: ignore [missing-import]
from selenium.webdriver.support.ui import Select, WebDriverWait
from urllib.parse import urlparse, urlunparse
import re
import operator
import random

# username = "usernametest"
# password = "Asdfghjkl@2026"

def fill(driver, id, value):
    element = driver.find_element(By.ID, id)
    element.clear()
    element.send_keys(value)
    
# driver = webdriver.Chrome()
# driver.maximize_window()
# wait = WebDriverWait(driver, 10)


def login(driver, username, password):
    logs.info(f"Executing login steps for {username}")
    wait = WebDriverWait(driver, 10)
    driver.get("https://site4people.com/welcome")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    # Fill form
    fill(driver, "username", username)
    fill(driver, "password", password)
    
    # Submit Button
    driver.find_element(By.XPATH, '//*[@id="login"]/div[5]/div[1]/button').click()
    
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

def logout(driver):
    current_url = driver.current_url
    logs.info(f"Logging out from current URL: {current_url}")

    if current_url.startswith("https://site4people.com/"):
        parsed_url = urlparse(current_url)
        
        # Reconstruct the URL with the new /logout/ path while keeping the original query
        new_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            '/logout/',       # New path
        parsed_url.params,
        parsed_url.query,  # Keeps 'cache=1787516726'
        parsed_url.fragment
    ))
    
    driver.get(new_url)
    logs.success("Logout command executed successfully.")
        
# login()