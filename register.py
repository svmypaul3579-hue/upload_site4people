# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 01:00:12 2026

@author: svmy
"""

import time

# pyrefly: ignore [missing-import]
from selenium import webdriver
# pyrefly: ignore [missing-import]
from selenium.webdriver.common.by import By
# pyrefly: ignore [missing-import]
from selenium.webdriver.support.ui import Select, WebDriverWait
import re
import operator
import random


def solve_captcha(text):
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv
    }

    a, op, b = re.search(r"(\d+)\s*([+\-*/])\s*(\d+)", text).groups()
    return ops[op](int(a), int(b))


def fill(driver, id, value):
    element = WebDriverWait(driver, 600).until(
        lambda d: d.find_element(By.ID, id)
    )

    element.clear()
    element.send_keys(value)


# username = "userxnetest"
# password = "Asdghjkl@2026"

# first_name = "Raghu"
# last_name = "Bearach"
# dof = "11-12-2000"

# driver = webdriver.Chrome()
# driver.maximize_window()

def register_user(driver, username, password, first_name, last_name, dof):
    random_num = str(random.randint(10000000, 99999999))
    phone_number = f"91{random_num}"
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://site4people.com/register")
        time.sleep(2)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        username = username.lower().replace(' ', '_')
        # Fill form
        fill(driver, "username", username)
        fill(driver, "email", f"{username}@site4people.com")
        fill(driver, "phone_num", phone_number)
        fill(driver, "password", password)
        fill(driver, "confirm_password", password)

        # Select gender
        Select(driver.find_element(By.ID, "gender")).select_by_value("male")

        # Solve captcha
        captcha_text = driver.find_element(By.CSS_SELECTOR, "label[for='captcha']").text
        fill(driver, "captcha", solve_captcha(captcha_text))

        # Accept terms
        driver.find_element(By.CSS_SELECTOR, "label[for='accept_terms']").click()

        time.sleep(2)  # Wait for a second before submitting
        # Submit
        driver.find_element(By.ID, "sign_submit").click()
        
        time.sleep(5)
        
        try:
            result_text = driver.find_element(By.XPATH, '//*[@id="register"]/div[1]').text
            
            if "This e-mail is already in use" in result_text:
                return False
        except:
            pass

    finally:
        # driver.quit()
        pass

    time.sleep(5)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    ## Next page

    skip_tag = driver.find_element(By.XPATH, '//*[@id="contnet"]/div/div[2]/div/div[3]/small')
    skip_tag.click()
    
    time.sleep(5)
    ## Next

    fill(driver, "first_name", first_name)
    fill(driver, "last_name", last_name)
    fill(driver, "usr_birthday", dof)

    # select contry
    Select(driver.find_element(By.ID, "country")).select_by_value('99')


    # click employeer

    driver.find_element(By.ID, 'employer-enabled').click()

    # save & Next

    driver.find_element(By.XPATH, "//button[contains(text(),'Save & Continue')]").click()
    
    time.sleep(5)
    ## Next (Final)
    try:
        driver.find_element(By.XPATH, "//button[contains(text(),'Finish')]").click()
    except:
        print("Finish button not found. Registration may not have completed successfully.")
        
    
    

# register_user(driver, username, password, first_name, last_name, dof)
