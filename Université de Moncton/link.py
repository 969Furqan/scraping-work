from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import csv

# List of URLs to scrape
urls = [
    "https://www.umoncton.ca/formation-continue/fr/programmes",
    "https://www.umoncton.ca/cycles_superieurs",
    "https://www.umoncton.ca/programmes"
]

# Initialize the webdriver
driver = webdriver.Chrome()

# Open the CSV file in write mode
with open('links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    for url in urls:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for and find all divs with id 'results2'
        results_divs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "results2"))
        )
        
        # Find all links within the results divs
        for div in results_divs:
            links = div.find_elements(By.TAG_NAME, "a")
            for link in links:
                # Write the href attribute to the CSV file
                href = link.get_attribute('href')
                writer.writerow([href])
