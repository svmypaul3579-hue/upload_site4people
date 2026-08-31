import re

import logs
from register import register_user
from login import login, logout
from create_page import create_page
from create_job import create_job
import time
import pandas as pd
# pyrefly: ignore [missing-import]
from selenium import webdriver
# pyrefly: ignore [missing-import]
from selenium.webdriver.common.by import By
# pyrefly: ignore [missing-import]
from selenium.webdriver.support.ui import Select, WebDriverWait
from datetime import datetime, timedelta
import random
import uuid
from discord import send_discord_message


def handle_selenium_error(driver, exception, context_msg):
    logs.error(f"Error caught: {context_msg} - {exception}")
    timestamp = int(time.time())
    screenshot_path = f"selenium_error_{timestamp}.png"
    try:
        if driver:
            driver.save_screenshot(screenshot_path)
            logs.info(f"Screenshot saved to {screenshot_path}")
        else:
            screenshot_path = None
    except Exception as se:
        logs.error(f"Failed to save screenshot: {se}")
        screenshot_path = None

    msg = (
        f"❌ Selenium Error/Crash in app.py!\n"
        f"Context: {context_msg}\n"
        f"Error: {type(exception).__name__}: {exception}"
    )
    send_discord_message(msg, file_paths=[screenshot_path] if screenshot_path else None)


leads_df = pd.read_csv("downloaded_sheet.csv", dtype=object)
save_df = pd.read_csv("data.csv", dtype=object)

leads_df = leads_df[leads_df['Company name'].notna() & leads_df['HR Name'].notna()]


# print(leads_df.columns.tolist())

def generate_birthdate_for_age_range(min_age=25, max_age=30):
    """Generates a random birth date for someone within a specific age range

    relative to today.
    """
    today = datetime.today()

    # 1. Calculate the absolute oldest and youngest possible birth dates
    # Someone who is 30 today was born exactly 30 years ago (+ leap year buffers)
    start_date = today.replace(year=today.year - max_age - 1) + timedelta(
        days=1
    )
    end_date = today.replace(year=today.year - min_age)

    # 2. Pick a random number of days between those two dates
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)

    # 3. Add the random days to the start date
    random_birthdate = start_date + timedelta(days=random_days)

    # Return as a string formatted as "DD-MM-YYYY"
    return random_birthdate.strftime("%d-%m-%Y")


# Example usage:
# print(generate_birthdate_for_age_range(25, 30))

def modify_csv_data(data, row_id=None, new_row_data=None):
    # 1. Ensure data is a DataFrame (loads file path if a string is passed)
    if isinstance(data, str):
        df = pd.read_csv(data, dtype=object)
    else:
        df = data.copy()

    # Empty columns are often inferred as float64 when they contain only NaN values.
    # That breaks later assignments like page_name = "self_employed__careers".
    df = df.where(pd.notna(df), None)
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].astype(object)

    # 2. Return early if no new data was provided
    if new_row_data is None:
        logs.warning("No new row data provided.")
        return df

    # 3. Logic: Update vs Add
    if row_id is not None:
        target_row = None

        if row_id in df.index:
            target_row = row_id
        elif "orginal_id" in df.columns and row_id in df["orginal_id"].tolist():
            target_row = df.index[df["orginal_id"] == row_id][0]
        elif "username" in df.columns and "username" in new_row_data:
            username_value = new_row_data["username"]
            if username_value in df["username"].tolist():
                target_row = df.index[df["username"] == username_value][0]

        if target_row is not None:
            for column, value in new_row_data.items():
                df.at[target_row, column] = value
            logs.success(f"Successfully updated row index: {target_row}")
        else:
            logs.error(f"Error: Row ID {row_id} does not exist.")
    else:
        # Append the new dictionary data as a new row at the bottom
        new_row_df = pd.DataFrame([new_row_data])
        df = pd.concat([df, new_row_df], ignore_index=True)
        logs.success("Successfully added a new row.")

    # 4. Save back to file automatically if a path was originally provided
    if isinstance(data, str):
        df.to_csv(data, index=False, na_rep="")

    return df

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', str(text))

def create_unique_id():
    # uuid4 generates a completely random unique ID
    return str(uuid.uuid4())

driver = None
try:
    for index, row in leads_df.iterrows():
        # Driver check & recovery
        try:
            if driver is None:
                driver = webdriver.Chrome()
                driver.maximize_window()
            else:
                try:
                    driver.title
                except Exception:
                    logs.warning("Selenium driver is unresponsive or closed. Re-initializing driver.")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    driver = webdriver.Chrome()
                    driver.maximize_window()
        except Exception as driver_err:
            logs.error(f"Failed to initialize/restart Chrome driver: {driver_err}")
            time.sleep(10)
            continue

        try:
            company_name = remove_special_characters(row['Company name'])
            name = remove_special_characters(row['HR Name'])
            # Convert name to a string to handle any accidental numbers or NaN values
            if pd.isna(name) or not str(name).strip():
                first_name = "name"
                last_name = "name"
            else:
                name_str = str(name).strip()
                first_name, last_name = name_str.split(' ', 1) if ' ' in name_str else (name_str, '')

                first_name = first_name or "name"
                last_name = last_name or "name"

            logs.info(f"Processing row {index}: Company Name: {company_name}, HR Name: {name}, First Name: {first_name}, Last Name: {last_name}")

            # Check if company name already exists in save_df
            existing_user = save_df[save_df['company_name'] == company_name]

            if not existing_user.empty:
                username = existing_user.iloc[0]['username']
                password = existing_user.iloc[0]['password']
                logs.info(f"Company '{company_name}' already exists. Fetched username: {username}")
            else:
                # Register user
                if name == "nan" or name == "" or pd.isna(name):
                    username = f"{company_name.lower().replace(' ', '_')}{index}"
                    password = f"{company_name.lower().replace(' ', '_')}@2026"
                else:
                    username = f"{first_name.lower()}{last_name.lower()}{index}"
                    password = f"{first_name.lower()}{last_name.lower()}{index}@2026"
                logs.info(f"Generated username: {username}")

                dof = generate_birthdate_for_age_range(25, 30)

                result = register_user(driver,
                    username, password, first_name, last_name, dof
                )

                # print(result)
                if result is False:
                    logs.error(f"Registration failed for username: {username}. Skipping to next row.")
                    continue

                logs.success(f"User registered successfully: {username}")
                logout(driver)

                ## update save_df
                save_df = modify_csv_data("data.csv", new_row_data={
                    'id': create_unique_id(),
                    'company_name': company_name,
                    'username': username.replace(' ', '_'),
                    'password': password,
                    'orginal_id': index,
                    'is_registered': True
                })
            # time.sleep(5)
            try:
                rows = save_df.loc[save_df['username'] == username, 'page_name']

                if rows.empty or rows.iloc[0] is None or pd.isna(rows.iloc[0]) or str(rows.iloc[0]).strip() == "":
                # if save_df.loc[save_df['username'] == username, 'page_name'].empty or save_df.loc[save_df['username'] == username, 'page_name'].iloc[0] is None:
                    logs.info(f"Page name is empty for username: {username}. Proceeding to create page.")
                    
                    logs.info(f"Attempting to log in with username: {username}")

                    login(driver, username, password)

                    modify_csv_data("data.csv", row_id=index, new_row_data={'is_login': True})
                    logs.success(f"Login successful for username: {username}")
                    time.sleep(5)
                    # create page

                    page_title = f"{company_name} Careers"
                    page_category = "Other"
                    index_id = save_df.index[save_df['username'] == username].tolist()[0]
                    page_description = f"Welcome to {company_name} Careers. We are hiring talented individuals to join our team. Explore our job opportunities and apply today!"
                    try:
                        page_name = create_page(driver, page_title, page_category, page_description)
                        if page_name is None:
                            raise RuntimeError("Page creation failed (create_page returned None)")
                        logs.success(f"Page created successfully: {page_name}")
                        page_id = f"https://site4people.com/{page_name}"
                        modify_csv_data("data.csv", row_id=index_id, new_row_data={'page_name': page_name, 'page_id': page_id, 'is_page_created': True})
                        logout(driver)
                    except Exception as e:
                        logs.error(f"Error updating CSV data for username: {username}. Error: {e}")
                        handle_selenium_error(driver, e, f"Page creation failed for username: {username}")
                        try:
                            logout(driver)
                        except Exception:
                            pass
            except Exception as e:
                logs.error(f"Login failed for username: {username}. Error: {e}")
                handle_selenium_error(driver, e, f"Login failed for username: {username}")
                try:
                    logout(driver)
                except Exception:
                    pass
                
            time.sleep(5)
        except Exception as row_err:
            logs.error(f"Unhandled error processing row {index} for company '{row.get('Company name')}': {row_err}")
            handle_selenium_error(driver, row_err, f"Unhandled error in row {index}")
            try:
                logout(driver)
            except Exception:
                pass
            time.sleep(5)
except Exception as e:
    logs.error(f"Fatal script crash: {e}")
    handle_selenium_error(driver, e, "Fatal unhandled crash/error in app.py script")
finally:
    if driver is not None:
        try:
            driver.quit()
        except Exception:
            pass


    