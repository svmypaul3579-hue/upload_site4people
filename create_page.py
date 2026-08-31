
from concurrent.futures import wait
import time
import logs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

categories = {
    "Cars and Vehicles": "2",
    "Comedy": "3",
    "Economics and Trade": "4",
    "Education": "5",
    "Entertainment": "6",
    "Gaming": "8",
    "History and Facts": "9",
    "Live Style": "10",
    "Movies & Animation": "7",
    "Natural": "11",
    "News and Politics": "12",
    "Other": "0",
    "People and Nations": "13",
    "Pets and Animals": "14",
    "Places and Regions": "15",
    "Science and Technology": "16",
    "Sport": "17",
    "Travel and Events": "18"
}


def fill(driver, id, value):
    element = driver.find_element(By.ID, id)
    element.clear()
    element.send_keys(value)


def wait_for_page_load(driver, timeout=30):
    try:
        wait = WebDriverWait(driver, timeout)

        # Check page is fully loaded
        wait.until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        # Check required element exists
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="contnet"]/div/div/div[1]/div/div/ul/li[14]/a')
            )
        )

        # All checks passed
        return True

    except Exception as e:
        logs.error(f"Page load check failed: {e}")
        return False

def adjust_page_name(page_title):
    page_name = page_title.lower().replace(' ', '_')

    # If too short, append "_page"
    if len(page_name) < 6:
        page_name = page_name + "_page"

    # If still too long, trim to 30 characters
    if len(page_name) > 30:
        page_name = page_name[:30]

    return page_name

# page_title = "Statistical Professor career"
# page_name = page_title.lower().replace(' ', '_')
# page_category = "Education"
# page_description = "we are hiring Statistical Professor. hurry up"


# driver = webdriver.Chrome()
# driver.maximize_window()
# wait = WebDriverWait(driver, 10)

def create_page(driver, page_title, page_category, page_description):
    page_name = adjust_page_name(page_title)
    try:
        driver.get("https://site4people.com/create-page")

        wait_for_page_load(driver)

        fill(driver, 'page_title', page_title)
        fill(driver, 'page_name', page_name)
        dropdown = Select(driver.find_element(By.ID, "page_category"))

        dropdown.select_by_value(categories[page_category])

        fill(driver, 'page_description', page_description)

        ## submit button
        time.sleep(5)  # Wait for a second before submitting
        driver.execute_script("window.scrollBy(0, 150);")
        driver.find_element(By.XPATH, '//*[@id="contnet"]/div/div/div[2]/div[2]/form/div[6]/button').click()
        
        time.sleep(15)  # Wait for the page to process the submission

        wait_for_page_load(driver)
        try:
            alert_text = driver.find_element(By.XPATH, '//*[@id="contnet"]/div/div/div[2]/div[2]/form/div[5]/div').text
            logs.info(f"Alert text: {alert_text}")
            if "Page name is already exists." in alert_text:
                logs.warning(f"Page name '{page_name}' already exists. Please choose a different name.")
                return page_name  # Return the page name for further use if needed
        except:
            pass  # No alert found, continue
        return page_name  # Return the page name for further use if needed

    except Exception as e:
        logs.error(f"Error creating page: {e}")

        return None  # Return None to indicate failure
