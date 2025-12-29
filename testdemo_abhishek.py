from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import random
import time
import re

# ---------- Config ----------
options = Options()
options.add_experimental_option("detach", True)  # Keep Chrome open after script ends

# ---------- Helper Functions ----------
def generate_random_email():
    username = "abi_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{username}@yopmail.com"

def generate_random_nepali_phone():
    # Start with 9, then 9 random digits
    return '9801' + ''.join(random.choices('0123456789', k=6))

# Example usage
random_nepali_number = generate_random_nepali_phone()
print(random_nepali_number)

# ---------- Start WebDriver ----------
driver = webdriver.Chrome(options=options)
driver.get("https://authorized-partner.vercel.app/")
wait = WebDriverWait(driver, 15)

# ---------- Step 1: Get Started ----------
get_started_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Get Started']"))
)
get_started_button.click()

# ---------- Step 2: I Agree ----------
get_iagree_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div[3]/div/button"))
)
get_iagree_button.click()

# ---------- Step 3: Continue ----------
get_continue_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a/button[normalize-space()='Continue']"))
)
get_continue_button.click()

# ---------- Step 4: Fill Personal Info ----------
# First Name
first_name_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Your First Name']"))
)
first_name_input.send_keys("Abhishek")

# Last Name
last_name_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Your Last Name']"))
)
last_name_input.send_keys("Bhandari")

# Email
email_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//input[@type='email' or contains(@placeholder,'Email')]"))
)
email = generate_random_email()
print("Generated email:", email)
email_input.clear()
email_input.send_keys(email)

# Phone Number
# Phone Number (Nepali 10-digit format)
number_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[2]/div/div/input"))
)

random_nepali_number = generate_random_nepali_phone()
print("Generated Nepali phone number:", random_nepali_number)

number_input.clear()
number_input.click()
number_input.send_keys(random_nepali_number)
time.sleep(2)

# Password
password_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[3]/div[1]/div[1]/input"))
)
password_input.send_keys("Testing123!")

# Confirm Password
confirm_password_input = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[3]/div[2]/div[1]/input"))
)
confirm_password_input.send_keys("Testing123!")

# Next Button
next_button_personal = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']"))
)
next_button_personal.click()

print("Form filled successfully!")


# ---------------- OPEN YOPMAIL ----------------
driver.execute_script("window.open('https://yopmail.com','_blank')")
driver.switch_to.window(driver.window_handles[1])
wait = WebDriverWait(driver, 30)

inbox = email.split("@")[0]

login_input = wait.until(EC.element_to_be_clickable((By.ID, "login")))
login_input.clear()
login_input.send_keys(inbox)
login_input.send_keys(Keys.RETURN)

# ---------------- OTP FETCH ----------------
otp = None

for attempt in range(1, 11):
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "ifmail")))

        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(body_text)

        match = re.search(r"code below:\s*(\d{4,6})", body_text, re.IGNORECASE)
        if match:
            otp = match.group(1)
            print("OTP Captured:", otp)
            break

    except:
        print("Waiting for OTP...")

    finally:
        driver.switch_to.default_content()

    driver.find_element(By.ID, "refresh").click()
    time.sleep(3)

if not otp:
    raise Exception("OTP not received")


# ---------------- OTP SUBMISSION (FINAL FIX) ----------------
driver.switch_to.window(driver.window_handles[0])
wait = WebDriverWait(driver, 30)

# Wait for Verify button (means OTP page loaded)
wait.until(EC.presence_of_element_located(
    (By.XPATH, "//button[contains(.,'Verify')]")
))

# Find OTP input (first visible enabled input)
otp_input = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/div/form/div[1]/div[2]/input")
    )
)

# Focus input
otp_input.click()
time.sleep(0.5)

# IMPORTANT: Clear properly
otp_input.send_keys(Keys.CONTROL + "a")
otp_input.send_keys(Keys.BACKSPACE)

# OTP Submission
for digit in otp:
    otp_input.send_keys(digit)
    time.sleep(0.2)   # REQUIRED for React state update

# Small wait for validation
time.sleep(1)

# Click Verify
verify_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[not(@disabled) and contains(.,'Verify')]")
    )
)

verify_button.click()

print("✅ OTP submitted successfully")


# ---------------- AGENCY DETAILS ----------------

agency_name = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[1]/div[1]/input")
    )
)
agency_name.send_keys("Authorized Agency")
agency_name.send_keys(Keys.RETURN)

role_agency = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[1]/div[2]/input")
    )
)
role_agency.send_keys("QA Intern")
role_agency.send_keys(Keys.RETURN)

email_agency = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[1]/input")
    )
)
email_agency.send_keys("authorizedpartner@yopmail.com")
email_agency.send_keys(Keys.RETURN)

website_agency = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[2]/div/input")
    )
)
website_agency.send_keys("www.linkedin.com")
website_agency.send_keys(Keys.RETURN)

agency_address = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[3]/div[1]/input")
    )
)
agency_address.send_keys("Imadol,Lalitpur")

agency_region = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@role='combobox' and .//span[text()='Select Your Region of Operation']]")
    )
)
agency_region.click()

# Click "Canada"
canada_option = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//div[normalize-space()='Canada']")
    )
)
canada_option.click()

next_button_agency = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[4]/button[2]")
    )
)
next_button_agency.click()

#------------- Professional Experience---------------

years_experience = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[1]/div[1]/button")
    )
)
years_experience.click()

#Click "1 Years"
one_year_experience = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"//div[normalize-space()='1 year']")
    )
)
one_year_experience.click()

student_recruited = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[1]/div[2]/input")
    )
)

student_recruited.send_keys("30")

focus_area = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[1]/input")
    )
)
focus_area.send_keys("Undergraduate")

success_percent = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[2]/div/input")
    )
)
success_percent.send_keys("90%")

service_provided = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[3]/div[2]/div[1]/button")
    )
)
service_provided.click()

next_button_experience = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[4]/button[2]")
    )
)

next_button_experience.click()

#--------------- Business Detail ---------------------

business_registration = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[1]/div[1]/input")

    )
)
business_registration.send_keys("321XXXXXXXXX4")

prefer_country = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[1]/div[2]/button/div/span")
    )
)
prefer_country.click()

#Select Country "Canada"

select_preference = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"//div[normalize-space()='Canada']")
        #(By.XPATH,"//div[normalize-space()='Australia']")

    )
)
select_preference.click()

institution_type = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[1]/div[2]/div[1]/button")
    )
)
institution_type.click()

certification_details = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[2]/div[2]/input")
    )
)
certification_details.send_keys("1234ABCDXXX")

upload_business = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[3]/div[1]/div/div")
    )
)
upload_business.click()


#driver.find_element(By.ID, "uploadBtn").click()

file_input = driver.find_element(By.XPATH, "//input[@type='file']")
file_input.send_keys("/Users/abhishekbhandari/Downloads/Task.pdf")


submit_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH,"/html/body/div[3]/div[4]/div/div/div/div[2]/form/div[4]/button[2]")
    )
)
submit_button.click()