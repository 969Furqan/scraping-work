import requests
from bs4 import BeautifulSoup
import csv

# URLs to scrape
urls = [
    "https://www.isu.edu/majors/",
    "https://www.isu.edu/graduateprograms/",
    "https://www.isu.edu/minors/",
    "https://www.isu.edu/certificates/"
]

# List to store the extracted links
extracted_links = []

# Function to extract links from a given URL
def extract_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', class_='stretched-link')
    for link in links:
        href = link.get('href')
        if href:
            extracted_links.append(href)

# Extract links from each URL
for url in urls:
    extract_links(url)

# Write the extracted links to a CSV file
with open('links.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for link in extracted_links:
        writer.writerow([link])