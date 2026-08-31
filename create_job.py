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

def select_category(driver, id, value):
    dropdown = Select(
        driver.find_element(By.ID, id)
    )

    dropdown.select_by_value(value)

def fill(driver, id, value):
        element = driver.find_element(By.ID, id)
        element.clear()
        element.send_keys(value)

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
def create_job(driver, page_id, job_type, job_title, location, job_area, job_state, max_salary, min_salary, salary_interval, job_exp_from, job_exp_to, job_skill_category, designation_name, job_skill_level, field_of_work, description):

    try:
        driver.get(f"https://site4people.com/{page_id}")

        driver.execute_script("OpenCreateJobModal();")

        time.sleep(2)
        # job type
        select_category(driver, 'job_type', jobType[job_type])
        # job title
        fill(driver, 'job_title', job_title)

        # work modes 
        workModes = Select(
            driver.find_element(By.XPATH, '//*[@id="normal-job-fields"]/div[1]/div[2]/div/select')
        )

        workModes.select_by_value(work_modes[location])

        # job area
        fill(driver, 'job_area', job_area)

        # job state
        select_category(driver, 'cjob_state', state_ids[job_state])

        time.sleep(2)
        # job city
        select_category(driver, 'cjob_city_autocomplete', '141916')

        # salary
        fill(driver, 'minimum', max_salary)
        fill(driver, 'maximum', min_salary)

        # salary period
        select_category(driver, 'salary_date', salary_period[salary_interval])

        #exprience

        fill(driver, 'job_exp_from', job_exp_from)
        fill(driver, 'job_exp_to', job_exp_to)

        # job skill category
        select_category(driver, 'job_skill_category', job_skill_category)

        # job skills
        skills = ["Content Writing", "Journalism", "Copywriting"]

        for skill in skills:
            job_skills = driver.find_element(
                By.CSS_SELECTOR,
                "#job_skills + span .select2-search__field"
            )

            job_skills.click()
            job_skills.send_keys(skill)
            time.sleep(0.5)
            job_skills.send_keys(Keys.ENTER)
            
        designation = Select(
            driver.find_element(By.XPATH, '//*[@id="normal-job-fields"]/div[7]/div/div/select')
        )

        designation.select_by_value(designation_name)

        # job skill level
        select_category(driver, 'job_skill_level', jobSkillLevel[job_skill_level])

        # field of work
        job_fow = Select(driver.find_element(By.ID, "job_fow"))

        if field_of_work in job_fow_options:
            job_fow.select_by_value(job_fow_options[field_of_work])
        else:
            driver.find_element(By.ID, "job_fow_cst_btn").click()

            job_fow_other = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "job_fow_other"))
            )

            job_fow_other.clear()
            job_fow_other.send_keys(field_of_work)
            
        # job description
        driver.switch_to.active_element.send_keys(Keys.TAB)
        driver.switch_to.active_element.send_keys(description)

        time.sleep(2)
        # final submit

        driver.find_element(By.XPATH, '//*[@id="createJOnfrm"]/div[2]/button').click()


        try:
            text = WebDriverWait(driver, 5).until(
                lambda d: (
                    d.find_element(
                        By.XPATH,
                        '//*[@id="createJOnfrm"]/div[1]/div[1]/div[1]'
                    ).text.strip()
                    or False
                )
            )

            logs.info(f"Result found: {text}")

        except Exception:
            logs.warning("No text found within 5 seconds. Continuing...")
    except Exception as e:
        logs.error(f"An error occurred while creating the job: {e}")
