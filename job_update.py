import os

# os.chdir(r'J:\code\working\malik\site4people\python')
from create_job import create_job
import time
import pandas as pd
import re
import unicodedata
import logs
from login import login, logout
# pyrefly: ignore [missing-import]
from selenium import webdriver
# pyrefly: ignore [missing-import]
from selenium.webdriver.common.by import By
# pyrefly: ignore [missing-import]
from selenium.webdriver.support.ui import Select, WebDriverWait
from discord import send_discord_message
from designation_matcher import find_best_designation_and_category

logs.highlight("Starting job_update script...")

logs.info("Loading job_leads.csv...")
job_leads_df = pd.read_csv("job_leads.csv", dtype=object)
job_leads_df['uploaded'] = (
    job_leads_df['uploaded']
    .astype(str)
    .str.strip()
    .str.lower()
    .eq('true')
)
total_leads = len(job_leads_df)
already_uploaded = job_leads_df['uploaded'].sum()
logs.info(f"Loaded {total_leads} job leads ({already_uploaded} already uploaded, {total_leads - already_uploaded} pending).")

logs.info("Loading data.csv...")
company_df = pd.read_csv("data.csv", dtype=object)
logs.info(f"Loaded {len(company_df)} companies from data.csv.")

logs.debug(f"Job leads columns: {job_leads_df.columns.tolist()}")

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
        f"❌ Selenium Error/Crash in job_update.py!\n"
        f"Context: {context_msg}\n"
        f"Error: {type(exception).__name__}: {exception}"
    )
    send_discord_message(msg, file_paths=[screenshot_path] if screenshot_path else None)

def remove_emojis_builtin(text: str) -> str:
    """Removes emojis using built-in Unicode character categories."""
    return "".join(
        char for char in text 
        if unicodedata.category(char) not in ("So", "Symbol, Other")
    )

logs.info("Initializing Chrome WebDriver...")
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)
logs.success("Chrome WebDriver initialized and window maximized.")

try:
    for index, row in job_leads_df.iterrows():
        job_title = row.get('job_title', 'Unknown Title')
        company_id = row.get('company_id')
        is_uploaded = row.get('uploaded', False)

        logs.info(f"=== Processing row [{index + 1}/{total_leads}] (Index: {index}) | Job: '{job_title}' | Company ID: {company_id} ===")

        if pd.isna(company_id):
            logs.warning(f"Row {index}: company_id is NaN. Skipping.")
            continue

        if is_uploaded:
            logs.info(f"Row {index}: Job '{job_title}' (Company ID: {company_id}) is already marked as uploaded. Skipping.")
            continue

        try:
            company_id = int(company_id)
            if company_id not in company_df.index:
                logs.warning(f"Row {index}: Company ID {company_id} not found in company_df. Skipping.")
                continue

            page_url = company_df.loc[company_id, 'page_id']
            username = company_df.loc[company_id, 'username']
            password = company_df.loc[company_id, 'password']

            if pd.isna(page_url) or not str(page_url).strip():
                logs.warning(f"Row {index}: Company ID {company_id} ({username}) has no valid page_id in data.csv. Skipping.")
                continue

            company_name = company_df.loc[company_id, 'company_name'] if 'company_name' in company_df.columns else 'Unknown'
            logs.info(f"Row {index}: Target company: '{company_name}' | Page URL: {page_url} | Username: {username}")
            login(driver, username, password)

            time.sleep(5)
            skills_list = row['skills'].split(',') if pd.notna(row['skills']) and str(row['skills']).strip() else []
            logs.debug(f"Row {index}: Finding designation for skills: {skills_list}")
            designation_result = find_best_designation_and_category(skills_list)
            logs.info(
                f"Row {index}: Matched designation '{designation_result.get('designation_value')}' "
                f"(Skill Category ID: {designation_result.get('skill_category_id')})"
            )

            raw_desc = row['descriptions'] if pd.notna(row['descriptions']) else ""
            clean_desc = remove_emojis_builtin(raw_desc)

            logs.info(f"Row {index}: Creating job '{job_title}' on {page_url}...")
            job_created = create_job(
                driver,
                page_url=page_url,
                job_type=row['job_type'],
                job_title=row['job_title'],
                location=row['location'],
                job_area=row['job_area'],
                job_state=row['job_state'],
                max_salary=row['max_salary'],
                min_salary=row['min_salary'],
                salary_interval=row['salary_interval'],
                job_exp_from=row['job_exp_from'] if pd.notna(row['job_exp_from']) else 0,
                job_exp_to=row['job_exp_to'] if pd.notna(row['job_exp_to']) else 0,
                job_skill_category=designation_result['skill_category_id'],
                designation_name=designation_result['designation_value'],
                job_skill_level=row['job_skill_level'],
                skills=skills_list,
                field_of_work=row['job_title'],
                description=clean_desc
            )

            if job_created:
                job_leads_df.at[index, 'uploaded'] = True
                job_leads_df.to_csv("job_leads.csv", index=False)
                logs.success(f"Row {index}: Job '{job_title}' uploaded successfully and recorded in job_leads.csv.")
            else:
                logs.error(f"Row {index}: Job creation failed for '{job_title}'. CSV not marked as uploaded.")

            logout(driver)

        except KeyError as ke:
            logs.error(f"Row {index}: Company ID {company_id} KeyError in company_df: {ke}. Skipping.")
        except Exception as e:
            logs.error(f"Row {index}: Error occurred while processing row: {e}")
            logs.print_traceback()
            handle_selenium_error(driver, e, f"Error processing row {index} for job '{job_title}'")
            try:
                logout(driver)
            except Exception:
                pass
        
        wait = WebDriverWait(driver, 20)
        
        # Check page is fully loaded
        try:
            wait.until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )
        except Exception as e:
            logs.warning(f"Row {index}: Document readyState wait encountered: {e}")

except Exception as fatal_err:
    logs.error(f"Fatal crash in job_update.py: {fatal_err}")
    logs.print_traceback()
    handle_selenium_error(driver, fatal_err, "Fatal script error in job_update.py")
finally:
    logs.highlight("Completed job_update execution.")

