import requests
from bs4 import BeautifulSoup
import csv

def extract_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the tbody with class 'list'
    tbody = soup.find('tbody', class_='list')

    # Extract all href links from <a> tags within the tbody
    links = []
    if tbody:
        for a_tag in tbody.find_all('a', href=True):
            links.append(a_tag['href'])

    return links

def save_links_to_csv(links, filename):
    # Write links to a CSV file without headers
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

if __name__ == "__main__":
    url = "https://durhamcollege.ca/programs-and-courses"
    links = extract_links(url)
    save_links_to_csv(links, 'links.csv')
    print(f"Extracted {len(links)} links and saved to links.csv")