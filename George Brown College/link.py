import requests
from bs4 import BeautifulSoup
import csv

def extract_program_links(url):
    # Send GET request to the URL
    response = requests.get(url)
    
    # Create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all 'a' tags with class 'program-title-link'
    program_links = soup.find_all('a', class_='program-title-link')
    
    # Extract href attributes from the tags
    links = [link.get('href') for link in program_links]
    
    # Write links to CSV file
    with open('links.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow(["https://www.georgebrown.ca"+link])

if __name__ == '__main__':
    # Replace with your target URL
    url = 'https://www.georgebrown.ca/program-finder?year=2024'
    extract_program_links(url)
