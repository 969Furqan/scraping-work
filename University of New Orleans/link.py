import requests
from bs4 import BeautifulSoup
import csv

# List of URLs to scrape
urls = [
    "https://www.uno.edu/academics/pre-professional-programs",
    "https://www.uno.edu/academics/online-programs",
    "https://www.uno.edu/academics/undergraduate-programs"
]

# Base URL to append
base_url = "https://www.uno.edu"

# List to store the links
links = []

# Loop through each URL
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all anchor tags within divs with class 'paragraph'
    for div in soup.find_all('div', class_='paragraph'):
        for a in div.find_all('a', href=True):
            full_link = base_url + a['href']
            links.append(full_link)

# Write the links to a CSV file
with open('links.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for link in links:
        writer.writerow([link])