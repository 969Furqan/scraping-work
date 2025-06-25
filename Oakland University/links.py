from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time  # Import the time module

# Define the URL of the webpage to scrape
url = "https://www.oakland.edu/academics/"  # Replace with the actual URL

# Set up the Selenium WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()  # You can use other drivers like Firefox, Edge, etc.

# Open the webpage
driver.get(url)

# Wait for 3 seconds
time.sleep(3)

# Find the tbody tag with the id 'table-body'
try:
    tbody = driver.find_element(By.ID, "table-body")
except:
    tbody = None

# Initialize a list to store the href links
links = []

# Extract all hrefs within the tbody if it exists
if tbody:
    a_tags = tbody.find_elements(By.TAG_NAME, "a")
    for a_tag in a_tags:
        href = a_tag.get_attribute("href")
        if href:
            links.append(href)
else:
    print("No tbody with id 'table-body' found.")

# Write the links to a CSV file
output_file = "links.csv"
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for link in links:
        writer.writerow([link])

print(f"Extracted {len(links)} links and saved to {output_file}.")

# Close the WebDriver
driver.quit()
