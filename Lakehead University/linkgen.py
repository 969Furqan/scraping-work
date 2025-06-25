import requests
from bs4 import BeautifulSoup
import csv

urls = [
    'https://www.lakeheadu.ca/programs/graduate/programs/diploma',
    'https://www.lakeheadu.ca/programs/undergraduate-programs',
    'https://www.lakeheadu.ca/programs/graduate/programs/masters',
    'https://www.lakeheadu.ca/programs/graduate/programs/doctoral/'
]

links = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all 'a' tags with class 'title'
    title_links = soup.find_all('a', class_='title')
    
    # Extract href and text from each link
    for link in title_links:
        links.append(["https://www.lakeheadu.ca"+link.get('href')])

# Write to CSV without headers
with open('links.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(links)
