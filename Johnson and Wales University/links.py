from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if you don't need the UI

# Setup ChromeDriver service
service = Service(ChromeDriverManager().install())

# Automatically download and manage the appropriate WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = 'https://www.jwu.edu/academics/programs/explore-programs.html?'

# Load the page
driver.get(url)

# Give the page time to load dynamically (you can adjust the sleep time if needed)
time.sleep(5)

# Find the <ul> with the class 'finder__list' and extract all <a> tags inside it
finder_list = driver.find_element(By.CLASS_NAME, 'finder__list')
anchor_tags = finder_list.find_elements(By.TAG_NAME, 'a')

# Initialize dictionaries to store the links for each location
locations = {
    'links': []
}

# Loop through all extracted <a> tags and sort them based on the text
for anchor in anchor_tags:
    text = anchor.text.strip().lower()  # Get the text and make it lowercase for case-insensitive matching
    href = anchor.get_attribute('href')  # Get the href attribute

    # Check for matching keywords in the text
    if 'providence' in text:
        locations['links'].append(href)
    elif 'charlotte' in text:
        locations['links'].append(href)
    elif 'online' in text:
        locations['links'].append(href)

# Save the links for each location to their respective CSV files
for location, links in locations.items():
    if links:  # Only save if there are links to store
        filename = f'{location}_links.csv'
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for link in links:
                    writer.writerow([link])
            print(f"Saved {filename}")
        except Exception as e:
            print(f"Error saving {filename}: {e}")

# Close the driver after scraping
driver.quit()
