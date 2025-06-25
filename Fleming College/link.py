from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def scrape_links(url):
    try:
        # Initialize Chrome webdriver
        driver = webdriver.Chrome()
        
        # Navigate to URL
        driver.get(url)
        
        # Wait for elements to be present
        wait = WebDriverWait(driver, 10)
        links = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a.stretched-link")
        ))
        
        # Extract href attributes
        href_list = [link.get_attribute('href') for link in links]
        
        # Write links to CSV file
        with open('links.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for href in href_list:
                writer.writerow([href])
                
        # Close browser
        driver.quit()
                
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'driver' in locals():
            driver.quit()

# Example usage - replace with your target URL
url = 'https://flemingcollege.ca/programs/a-z'  # Removed ?#a fragment
scrape_links(url)
