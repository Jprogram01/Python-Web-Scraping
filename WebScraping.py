import requests
from bs4 import BeautifulSoup
import mechanicalsoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import *
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

global joblistings
joblistings = []

job_search = input("What type of job would you like to search for? ")
location = input("In what location would you like to search for that job? (Can be 'Remote') ")

url = f"https://www.indeed.com/jobs?q={job_search}&l={location}&from=searchOnHP&vjk=ce9185b5c60f37dc"

def get_all_job_listings(url):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)
    
    try:
        iteration = 1
        while True:
            driver.get(url)
            iteration += 1
            # Wait for the next page link to be clickable
            time.sleep(5)
            next_page = driver.find_element(By.CSS_SELECTOR, (f"a[data-testid='pagination-page-{iteration}']"))
            
            jobs = driver.find_elements(By.CSS_SELECTOR, "h2[class*='jobTitle']")
            
            for job in jobs:
                try:
                    child_element = job.find_element(By.XPATH, "*")
                    parent_element = job.find_element(By.XPATH, "..")
                    sibling_element = parent_element.find_element(By.XPATH, "following-sibling::*")
                    sibling_child_element = sibling_element.find_element(By.XPATH, "*")
                    sibling_child_child_element = sibling_child_element.find_elements(By.XPATH, "*")
                    posting = [job.text, sibling_child_child_element[0].text, child_element.get_attribute("href")]
                    joblistings.append(posting)
                except NoSuchElementException:
                    # Handle if any element is not found on the current job listing
                    pass
                except AttributeError:
                    pass
            
            
            url = next_page.get_attribute("href")
    
    except NoSuchElementException:
        print(f"No more pages. Reached the end.")
    
    except NoSuchWindowException:
        print(f"Window Closed. Ending.")
    
    finally:
        driver.quit()


get_all_job_listings(url)
for i in joblistings:
    print(f"{i} \n")
print(len(joblistings))