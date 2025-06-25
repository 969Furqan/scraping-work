from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def extract_links():
    base_url = "https://www.canadorecollege.ca/programs/search?search=&page={}&is_v=1"
    links = []

    # Initialize Chrome driver
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Loop through all 43 pages
        for page in range(0, 44):
            url = base_url.format(page)
            driver.get(url)
            
            # Wait for elements to load
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "hit-link")))
            
            # Find all <a> tags with class 'hit-link'
            a_tags = driver.find_elements(By.CLASS_NAME, "hit-link")
            
            for a_tag in a_tags:
                link = a_tag.get_attribute('href')
                if link:
                    links.append(link)
            
            # Small delay to prevent overwhelming the server
            time.sleep(1)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

    # Write links to a CSV file without headers
    with open('links.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

if __name__ == "__main__":
    extract_links()