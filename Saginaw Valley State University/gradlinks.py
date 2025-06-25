import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Define the base URL and output file
base_url = "https://www.svsu.edu"
output_file = "links.csv"  # Path to your output CSV file

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Fetch the webpage content
driver.get(base_url)

# Initialize a list to store the href links
links = []

# Extract links from the specified div classes
for div_class in ["cards-graduate", "cards-undergrad"]:
    divs = driver.find_elements(By.CLASS_NAME, div_class)
    for div in divs:
        a_tags = div.find_elements(By.TAG_NAME, "a")
        for a_tag in a_tags:
            href = a_tag.get_attribute("href").strip()
            if not href.startswith("http"):
                href = base_url + href
            links.append(href)

# Write the links to a CSV file
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for link in links:
        writer.writerow([link])

print(f"Extracted {len(links)} links and saved to {output_file}.")

# Close the WebDriver
driver.quit()
