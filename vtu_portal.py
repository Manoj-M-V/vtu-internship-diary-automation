from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import shutil

from config import EMAIL, PASSWORD

class VTUPortal:
    def __init__(self):
        try:
            # Set up Chrome options for stability
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Initialize driver with correct ChromeDriver path
            print("Initializing ChromeDriver...")
            
            # First try: Get path from webdriver-manager and correct it
            try:
                manager_path = ChromeDriverManager().install()
                print(f"ChromeDriver manager path: {manager_path}")
                
                # webdriver-manager returns path to the .zip file or wrong file
                # The actual executable is in the chromedriver-win32 subdirectory
                if "chromedriver-win32" not in manager_path:
                    # Construct the path to the actual executable
                    base_path = os.path.dirname(manager_path)
                    chromedriver_exe = os.path.join(base_path, "chromedriver-win32", "chromedriver.exe")
                else:
                    chromedriver_exe = manager_path
                
                # Fallback: Check if the path exists, if not try to find it
                if not os.path.exists(chromedriver_exe):
                    # Search for chromedriver.exe in the cache
                    cache_dir = os.path.expanduser("~/.wdm")
                    for root, dirs, files in os.walk(cache_dir):
                        if "chromedriver.exe" in files:
                            chromedriver_exe = os.path.join(root, "chromedriver.exe")
                            print(f"Found chromedriver.exe at: {chromedriver_exe}")
                            break
                
                print(f"Using ChromeDriver at: {chromedriver_exe}")
                
                if not os.path.exists(chromedriver_exe):
                    raise FileNotFoundError(f"ChromeDriver executable not found at {chromedriver_exe}")
                
                service = Service(chromedriver_exe)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("ChromeDriver initialized successfully")
            except Exception as inner_error:
                print(f"Error with webdriver-manager path: {inner_error}")
                # Last resort: try without service specification
                print("Attempting to initialize without explicit service path...")
                self.driver = webdriver.Chrome(options=chrome_options)
                print("ChromeDriver initialized successfully (default path)")
        except Exception as e:
            print(f"Error initializing ChromeDriver: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        self.base_url = "https://vtu.internyet.in/"
        self.login_url = self.base_url + "sign-in"

    def login(self):
        try:
            print("Step 1: Navigating to base URL...")
            self.driver.get(self.base_url)
            print(f"Loaded: {self.base_url}")
            
            try:
                print("Step 2: Looking for sign-in link...")
                # Wait for the sign-in link to be clickable and click it
                sign_in_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='/sign-in']"))
                )
                sign_in_link.click()
                print("Sign-in link clicked")
            except:
                # Maybe already on the sign in page
                print("Sign-in link not found, might already be on sign-in page")
                pass

            print("Step 3: Finding email and password fields...")
            # Now on the login page, wait for the email input field to be present
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your email address']"))
            )
            password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Sign In')]")
            print("Email, password and login button found")

            print("Step 4: Entering credentials...")
            email_input.send_keys(EMAIL)
            password_input.send_keys(PASSWORD)
            print("Credentials entered")
            
            print("Step 5: Clicking login button...")
            login_button.click()
            print("Login button clicked")
            
            print("Step 6: Waiting for dashboard...")
            # Wait for the dashboard to load by checking for a known element on the dashboard
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Applied Internships')]"))
            )
            print("Dashboard loaded successfully")
        except Exception as e:
            print(f"An error occurred during login: {e}")
            import traceback
            traceback.print_exc()
            self.driver.save_screenshot("error_login.png")

    def go_to_diary_page(self, skip_login=False):
        print("Going to diary page...")
        if not skip_login:
            self.login()
        print("Logged in, now navigating to diary page...")
        diary_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/dashboard/student/student-diary']"))
        )
        self.driver.execute_script("arguments[0].click();", diary_link)
        print("Diary link clicked")
        
        # Wait for page to load
        time.sleep(3)
        
        # Take a screenshot to see what's on the page
        self.driver.save_screenshot("diary_page_loaded.png")
        print("Screenshot saved: diary_page_loaded.png")
        
        # Debug: print page title and check for the form
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")
        
        # Check what forms are on the page
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        print(f"Found {len(forms)} forms on page")
        for i, form in enumerate(forms):
            form_id = form.get_attribute("id")
            form_name = form.get_attribute("name")
            print(f"  Form {i}: id={form_id}, name={form_name}")
        
        # Try to find the form - it's check-diary-form
        print("Waiting for diary form...")
        form = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "check-diary-form"))
        )
        print("Diary form loaded")

    def fill_diary_entry(self, date, diary_data):
        """
        Two-step form submission:
        Step 1: Select internship and date in check-diary-form, click Continue
        Step 2: Fill actual form fields (work_summary, hours_worked, learnings, skills), click Save
        """
        try:
            print(f"\n=== STEP 1: Select Internship & Date ===")
            
            # Find the internship select element
            print("Step 1a: Selecting internship (Morgan Stanley)...")
            internship_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "internship_id"))
            )
            
            # Get the selected option value
            option = internship_select.find_element(By.TAG_NAME, "option")
            internship_value = option.get_attribute("value")
            print(f"  Found internship value: {internship_value}")
            
            # Set the value using JavaScript
            self.driver.execute_script(f"arguments[0].value = '{internship_value}';", internship_select)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                internship_select
            )
            print("  [OK] Internship selected")
            
            time.sleep(1)
            
            # Now select the date
            print(f"Step 1b: Selecting date {date.strftime('%Y-%m-%d')}...")
            
            # Debug: Let's see what buttons are available
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "check-diary-form"))
            )
            all_buttons = form.find_elements(By.TAG_NAME, "button")
            print(f"  Available buttons: {len(all_buttons)}")
            for i, btn in enumerate(all_buttons):
                btn_text = btn.text.strip()
                btn_type = btn.get_attribute("type")
                print(f"    Button {i}: text='{btn_text}', type='{btn_type}'")
            
            # Find and click the date picker button - might not have "Pick a Date" text
            date_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pick a Date') or contains(text(), 'Date') or contains(@data-slot, 'popover')]"))
            )
            self.driver.execute_script("arguments[0].click();", date_button)
            print("  Date picker opened")
            
            time.sleep(1)
            
            # Click the specific date in the calendar
            day = date.day
            date_day_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'rdp-day') and text()='{day}']"))
            )
            self.driver.execute_script("arguments[0].click();", date_day_button)
            print(f"  [OK] Date {day} selected")
            
            time.sleep(1)
            
            # Close the date picker if still open
            try:
                self.driver.execute_script("document.activeElement.blur();")
            except:
                pass
            
            time.sleep(1)
            
            # Click the Continue button to go to step 2
            print("Step 1c: Clicking Continue button...")
            continue_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            )
            self.driver.execute_script("arguments[0].click();", continue_button)
            print("  [OK] Continue clicked, waiting for form page...")
            
            time.sleep(3)  # Wait for page transition
            
            self.driver.save_screenshot("form_page.png")
            print("  Screenshot saved: form_page.png")
            
            print(f"\n=== STEP 2: Fill Form & Submit ===")
            
            # Now we should be on the form page with student-diary-form
            print("Step 2a: Waiting for form to load...")
            form = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "student-diary-form"))
            )
            print("  [OK] Form loaded")
            
            time.sleep(1)
            
            # Fill work summary
            print("Step 2b: Filling work summary...")
            work_textarea = self.driver.find_element(By.NAME, "description")
            work_textarea.clear()
            work_textarea.send_keys(diary_data["work_summary"])
            print(f"  [OK] Work summary filled")
            
            # Fill hours worked
            print("Step 2c: Filling hours worked...")
            hours_input = self.driver.find_element(By.XPATH, "//input[@type='number']")
            hours_input.clear()
            hours_input.send_keys(str(diary_data["hours_worked"]))
            print(f"  [OK] Hours worked filled: {diary_data['hours_worked']}")
            
            # Fill learnings
            print("Step 2d: Filling learnings/outcomes...")
            learnings_textarea = self.driver.find_element(By.NAME, "learnings")
            learnings_textarea.clear()
            learnings_textarea.send_keys(diary_data["learnings_outcomes"])
            print(f"  [OK] Learnings filled")
            
            # Handle skills dropdown (React Select)
            print("Step 2e: Selecting skills...")
            skill_name = diary_data.get("skills", "Java")
            
            try:
                # Find and click the React Select input
                skills_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@role='combobox' and contains(@id, 'react-select')]"))
                )
                print(f"  Found skills input")
                self.driver.execute_script("arguments[0].click();", skills_input)
                time.sleep(0.7)
                
                # Type to search/filter
                skills_input.send_keys(skill_name)
                print(f"  Typed '{skill_name}' in skills input")
                time.sleep(0.7)
                
                # Click the matching option
                try:
                    skill_option = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'react-select__option') and contains(text(), '{skill_name}')]"))
                    )
                    skill_option.click()
                    print(f"  [OK] Skill '{skill_name}' selected")
                except Exception as skill_select_error:
                    print(f"  Error finding skill option: {skill_select_error}")
                    print(f"  Trying alternative selector...")
                    # Try alternative selector
                    skill_option = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{skill_name}')]"))
                    )
                    skill_option.click()
                    print(f"  [OK] Skill '{skill_name}' selected (alternative)")
                
                # Wait for dropdown to fully close and settle
                time.sleep(1.5)
                
                # Click somewhere on the form to ensure dropdown closes completely
                try:
                    main_form = self.driver.find_element(By.ID, "student-diary-form")
                    self.driver.execute_script("arguments[0].click();", main_form)
                    time.sleep(0.5)
                except:
                    pass
            except Exception as skill_error:
                print(f"  ERROR selecting skills: {skill_error}")
                self.driver.save_screenshot("error_skills.png")
                raise
            
            # Optional: Fill reference links if provided
            if diary_data.get("links"):
                try:
                    links_textarea = self.driver.find_element(By.NAME, "links")
                    links_textarea.clear()
                    links_textarea.send_keys(diary_data["links"])
                    print(f"  [OK] Reference links filled")
                except:
                    pass
            
            # Optional: Fill blockers if provided
            if diary_data.get("blockers"):
                try:
                    blockers_textarea = self.driver.find_element(By.NAME, "blockers")
                    blockers_textarea.clear()
                    blockers_textarea.send_keys(diary_data["blockers"])
                    print(f"  [OK] Blockers filled")
                except:
                    pass
            
            # Final wait before submitting - ensure all fields and dropdowns are settled
            print("Step 2f: Final wait before submission...")
            time.sleep(2)
            
            # Submit the form
            print("Step 2g: Submitting form...")
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and (contains(text(), 'Save') or contains(text(), 'Submit'))]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("  [OK] Submit button clicked")
            
            time.sleep(2)
            
            # Check for success
            try:
                self.driver.save_screenshot("submission_result.png")
                print("  Screenshot saved: submission_result.png")
                print(f"\n[SUCCESS] Diary entry for {date.strftime('%Y-%m-%d')} submitted successfully!\n")
            except:
                pass

        except Exception as e:
            print(f"\n[ERROR] Error during form submission: {e}")
            import traceback
            traceback.print_exc()
            self.driver.save_screenshot(f"error_diary_{date}.png")
            raise

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    portal = VTUPortal()
    portal.go_to_diary_page()
    today = datetime.date.today()
    diary_content = generate_diary_entry(today)
    portal.fill_diary_entry(today, diary_content)
    portal.close()
