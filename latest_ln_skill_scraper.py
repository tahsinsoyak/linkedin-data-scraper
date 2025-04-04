import itertools
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the WebDriver
# for crome driver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.linkedin.com/login")

# Log in to LinkedIn
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

username.send_keys("test@gmail.com")
password.send_keys("test")
password.send_keys(Keys.RETURN)
# Give some time to load the page
time.sleep(5)

# Navigate to your profile and click "Add Skill"
driver.get("https://www.linkedin.com/in/hasan-h%C3%BCseyin-a918a526a/")
time.sleep(3)

# Click on the "Add skill" button
add_skill_button = driver.find_element(By.ID, "navigation-add-edit-deeplink-add-skills")
add_skill_button.click()
time.sleep(3)
# List of letters to create two-letter combinations
letters = 'abcdefghijklmnopqrstuvwxyz'

# Combine single letters and two-letter combinations
combinations = list(letters) + [''.join(pair) for pair in itertools.product(letters, repeat=2)]

# Set to store unique skills
skills_set = set()

# Open the file for writing
with open('skills2.txt', 'w', encoding='utf-8') as f:
    # Locate the skill input element and perform the operations
    for combo in combinations:
        try:
            # Wait for the skill input element to be present
            skill_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "single-typeahead-entity-form-component-profileEditFormElement-SKILL-AND-ASSOCIATION-skill-ACoAAEH70c0B8yOPV-FrzcUoVhl43rV8ebYrk8s-1-name"))
            )
            
            # Clear the input field and enter the two-letter combination
            skill_input.clear()
            time.sleep(0.1)
            skill_input.send_keys(combo)
            time.sleep(1.5)  # Wait for the suggestions to load

            # Extract the skill suggestions
            skills = driver.find_elements(By.XPATH, "//div[@role='option']")

            for skill in skills:
                skill_text = skill.text.strip()
                if skill_text:
                    if skill_text not in skills_set:
                        skills_set.add(skill_text)
                        # Write the new skill to the file
                        f.write(f"{skill_text}\n")

        except selenium.common.exceptions.StaleElementReferenceException:
            print(f"Encountered StaleElementReferenceException, retrying for combo: {combo}")
            continue  # Skip this combination and continue with the next one
        
        except selenium.common.exceptions.ElementNotInteractableException:
            print(f"ElementNotInteractableException encountered, skipping combo: {combo}")
            continue

        except selenium.common.exceptions.NoSuchElementException:
            print(f"NoSuchElementException encountered, skipping combo: {combo}")
            continue

# Clean up
driver.quit()

print(f"Total unique skills collected: {len(skills_set)}")