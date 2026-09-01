
import logs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
jobType = {
    "Full time": "full_time",
    "Part time": "part_time",
    "Internship": "internship",
    "Volunteer": "volunteer",
    "Contract": "contract"
}

work_modes = {
    "On-Site": "On-Site",
    "WFH": "WFH",
    "Hybrid": "Hybrid",
    "Field Job": "Field Job"
}

state_ids = {
    "Meghalaya": "4006",
    "Haryana": "4007",
    "Maharashtra": "4008",
    "Goa": "4009",
    "Manipur": "4010",
    "Puducherry": "4011",
    "Telangana": "4012",
    "Odisha": "4013",
    "Rajasthan": "4014",
    "Punjab": "4015",
    "Uttarakhand": "4016",
    "Andhra Pradesh": "4017",
    "Nagaland": "4018",
    "Lakshadweep": "4019",
    "Himachal Pradesh": "4020",
    "Delhi": "4021",
    "Uttar Pradesh": "4022",
    "Andaman and Nicobar Islands": "4023",
    "Arunachal Pradesh": "4024",
    "Jharkhand": "4025",
    "Karnataka": "4026",
    "Assam": "4027",
    "Kerala": "4028",
    "Jammu and Kashmir": "4029",
    "Gujarat": "4030",
    "Chandigarh": "4031",
    "Dadra and Nagar Haveli and Daman and Diu": "4033",
    "Sikkim": "4034",
    "Tamil Nadu": "4035",
    "Mizoram": "4036",
    "Bihar": "4037",
    "Tripura": "4038",
    "Madhya Pradesh": "4039",
    "Chhattisgarh": "4040",
    "Ladakh": "4852",
    "West Bengal": "4853"
}

salary_period =  {
    "Per Month": "per_month",
    "Per Hour": "per_hour",
    "Per Day": "per_day",
    "Per Week": "per_week",
    "Per Year": "per_year"
}

jobSkillLevel = {
    "Basic": "basic",
    "Intermediate": "intermediate",
    "Advanced": "advanced"
}

job_fow_options = {
    "Computers": "2",
    "IT": "4",
    "Software": "5"
}

def wait_for_page_load(driver, timeout=30):
    logs.debug("Waiting for page load completion...")
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
        logs.debug("Page load checks passed successfully.")
        return True

    except Exception as e:
        logs.error(f"Page load check failed: {e}")
        return False

def select_category(driver, id, value):
    dropdown = Select(
        driver.find_element(By.ID, id)
    )

    dropdown.select_by_value(str(value))

def fill(driver, id, value):
        element = driver.find_element(By.ID, id)
        element.clear()
        element.send_keys(str(value))

# driver = webdriver.Chrome()
# driver.maximize_window()
# wait = WebDriverWait(driver, 10)

# page_id = "statistical_professor"
# ## Job Details

# job_type = "Part time"
# job_title = "Asistance clerk"
# location = "On-Site"
# job_area = 'Kolkata'
# job_state = 'West Bengal'
# max_salary = 20000
# min_salary = 10000
# salary_interval = 'Per Month'
# job_exp_from = 0
# job_exp_to = 2
# job_skill_category = '58'
# designation_name = '675'
# job_skill_level = 'Intermediate'
# field_of_work = "Daily Work"
# description = "job description we are hiring, hurry up"

def create_job(driver, page_url, job_type, job_title, location, job_area, job_state, max_salary, min_salary, salary_interval, job_exp_from, job_exp_to, skills, job_skill_category, designation_name, job_skill_level, field_of_work, description):
    logs.highlight(f"Starting job creation: '{job_title}' on {page_url}")
    logs.info(
        f"Job parameters -> Type: {job_type}, Work Mode: {location}, Area: {job_area}, State: {job_state}, "
        f"Salary: {min_salary}-{max_salary}/{salary_interval}, Exp: {job_exp_from}-{job_exp_to} yrs, "
        f"Category: {job_skill_category}, Designation: {designation_name}, Level: {job_skill_level}, "
        f"Field of Work: {field_of_work}, Skills: {skills}"
    )
    try:
        logs.info(f"Navigating to page URL: {page_url}")
        driver.get(f"{page_url}")

        logs.info("Executing OpenCreateJobModal()...")
        driver.execute_script("OpenCreateJobModal();")

        time.sleep(2)
        # job type
        try:
            val = jobType.get(job_type, job_type)
            select_category(driver, 'job_type', val)
            logs.debug(f"Selected job type: {job_type} ({val})")
        except KeyError:
            logs.error(f"Invalid job type: {job_type}")
        except Exception as e:
            logs.error(f"Error selecting job type '{job_type}': {e}")

        # job title
        try:
            fill(driver, 'job_title', job_title)
            logs.debug(f"Filled job title: '{job_title}'")
        except Exception as e:
            logs.error(f"Error filling job title: {e}")

        # work modes 
        try:
            work_mode_val = work_modes.get(location, location)
            workModes = Select(
                driver.find_element(By.XPATH, '//*[@id="normal-job-fields"]/div[1]/div[2]/div/select')
            )

            workModes.select_by_value(work_mode_val)
            logs.debug(f"Selected work mode: {location} ({work_mode_val})")
        except Exception as e: 
            logs.error(f"Invalid work mode: {location}. Error: {e}")
        
        time.sleep(2)
        # job area
        try:
            fill(driver, 'job_area', job_area)
            logs.debug(f"Filled job area: '{job_area}'")
        except Exception as e:
            logs.error(f"Error filling job area: {e}")

        # job state
        try:
            state_val = state_ids.get(job_state, job_state)
            select_category(driver, 'cjob_state', state_val)
            logs.debug(f"Selected job state: {job_state} ({state_val})")
        except Exception as e:
            logs.error(f"Invalid job state: {job_state}. Error: {e}")

        time.sleep(2)
        # job city
        try:
            select_category(driver, 'cjob_city_autocomplete', '141916')
            logs.debug("Selected job city (141916)")
        except Exception as e:
            logs.error(f"Error selecting job city: {e}")

        # salary
        try:
            fill(driver, 'minimum', max_salary)
            fill(driver, 'maximum', min_salary)
            logs.debug(f"Filled salary fields: minimum={max_salary}, maximum={min_salary}")
        except Exception as e:
            logs.error(f"Error filling salary fields: {e}")

        # salary period
        try:
            salary_interval_val = salary_period.get(salary_interval, salary_interval)
            select_category(driver, 'salary_date', salary_interval_val)
            logs.debug(f"Selected salary interval: {salary_interval} ({salary_interval_val})")
        except Exception as e:
            logs.error(f"Invalid salary interval: {salary_interval}. Error: {e}")

        #exprience
        try:
            # Convert empty values to None
            job_exp_from = None if job_exp_from in [None, ""] else int(job_exp_from)
            job_exp_to = None if job_exp_to in [None, ""] else int(job_exp_to)

            # Both values are missing
            if job_exp_from is None and job_exp_to is None:
                job_exp_from = 0
                job_exp_to = 1

            # From is missing, To exists
            elif job_exp_from is None:
                job_exp_from = 0
                # Ensure job_exp_to is greater than job_exp_from
                if job_exp_to <= job_exp_from:
                    job_exp_to = job_exp_from + 1

            # To is missing, From exists
            elif job_exp_to is None:
                job_exp_to = job_exp_from + 1

            # Both exist but To is less than or equal to From
            elif job_exp_to <= job_exp_from:
                logs.warning(
                    f"job_exp_to ({job_exp_to}) is less than or equal to "
                    f"job_exp_from ({job_exp_from}). "
                    f"Adjusting job_exp_to to {job_exp_from + 1}."
                )
                job_exp_to = job_exp_from + 1

            fill(driver, 'job_exp_from', job_exp_from)
            fill(driver, 'job_exp_to', job_exp_to)
            logs.debug(f"Filled experience: from {job_exp_from} to {job_exp_to}")

        except Exception as e:
            logs.error(f"Error filling experience fields: {e}")

        # job skill category
        try:
            select_category(driver, 'job_skill_category', str(job_skill_category))
            logs.debug(f"Selected job skill category: {job_skill_category}")
        except Exception as e:
            logs.error(f"Invalid job skill category: {job_skill_category}. Error: {e}")

        # job skills
        try:
            logs.info(f"Adding {len(skills)} skills: {skills}")
            added_skills_count = 0
            for skill in skills:
                skill_name = str(skill).strip()
                if not skill_name:
                    continue
                job_skills = driver.find_element(
                    By.CSS_SELECTOR,
                    "#job_skills + span .select2-search__field"
                )

                job_skills.click()
                job_skills.send_keys(skill_name)
                time.sleep(0.5)
                job_skills.send_keys(Keys.ENTER)
                time.sleep(0.5)  # Wait for the skill to be added before proceeding to the next one
                added_skills_count += 1
            logs.debug(f"Added {added_skills_count} skill tags.")
        except Exception as e:
            logs.error(f"Error selecting job skills: {e}")

        # designation
        try:       
            designation = Select(
                driver.find_element(By.XPATH, '//*[@id="normal-job-fields"]/div[7]/div/div/select')
            )

            designation.select_by_value(str(designation_name))
            logs.debug(f"Selected designation: {designation_name}")
        except Exception as e:
            logs.error(f"Error selecting job designation: {e}")

        # job skill level
        try:
            skill_level_val = jobSkillLevel.get(job_skill_level, job_skill_level)
            select_category(driver, 'job_skill_level', skill_level_val)
            logs.debug(f"Selected job skill level: {job_skill_level} ({skill_level_val})")
        except Exception as e:
            logs.error(f"Invalid job skill level: {job_skill_level}. Error: {e}")

        # field of work
        try:
            job_fow = Select(driver.find_element(By.ID, "job_fow"))
            job_fow.select_by_value("4")
            logs.debug("Selected field of work: 4 (IT)")
        except Exception as e:
            logs.error(f"Error selecting field of work: {e}")
            
        # job description
        try:
            # driver.switch_to.active_element.send_keys(Keys.TAB)
            # time.sleep(2)
            # driver.switch_to.active_element.send_keys(Keys.TAB)
            # driver.switch_to.active_element.send_keys(description)
            
            xpath = '/html/body/div[3]/div[2]/div[5]/div/div/form/div[1]/div[1]/div[4]/div[9]/textarea'

            textarea = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            textarea.click()
            textarea.clear()
            textarea.send_keys(description)
            logs.debug(f"Filled job description ({len(description) if description else 0} characters).")
        except Exception as e:
            logs.error(f"Error filling job description in active element: {e}")

        time.sleep(2)
        # final submit
        try:
            driver.find_element(By.XPATH, '/html/body/div[1]/div/a').click()
            logs.debug("Dismissed banner/overlay link.")
        except Exception:
            pass
        # input("Press Enter to submit the job form...")  # Wait for user input before submitting
        
        logs.info("Submitting job creation form...")
        try:
            button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="createJOnfrm"]/div[2]/button')
                )
            )
            button.click()
            logs.info("Clicked submit button.")
        except Exception as e:
            logs.error(f"Button not found or click failed: {e}")
        # time.sleep(10)  # Wait for the page to process the submission

        logs.info("Waiting for page ready state after submit...")
        wait = WebDriverWait(driver, 30)
        try:
            wait.until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )
        except Exception as e:
            logs.warning(f"ReadyState check encountered timeout or exception: {e}")

        try:
            logs.info("Checking for creation confirmation text...")
            text = WebDriverWait(driver, 30).until(
                lambda d: (
                    d.find_element(
                        By.XPATH,
                        '//*[@id="createJOnfrm"]/div[1]/div[1]/div[1]/div'
                    ).text.strip()
                    or False
                )
            )

            logs.info(f"Result found: {text}")
            if 'Job request successfully created.' in text:
                logs.success(f"Job request successfully created: '{job_title}'")
                return True
            else:
                logs.error(f"Unexpected result text: {text}")
                return False

        except Exception as e:
            logs.warning(f"No result confirmation text found within timeout: {e}. Continuing...")
            return False
    except Exception as e:
        logs.error(f"An error occurred while creating the job '{job_title}': {e}")
        logs.print_traceback()
        return False
