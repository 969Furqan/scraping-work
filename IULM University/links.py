import requests
from bs4 import BeautifulSoup
import csv

def extract_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the div with the specified class
        div = soup.find('div', class_='card-soup accordion-widget')
        
        # Extract all <a> tags within the div
        links = []
        if div:
            a_tags = div.find_all('a')
            for a in a_tags:
                href = a.get('href')
                if href:
                    links.append(href)
        
        # Write the links to a CSV file without headers
        with open('links.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for link in links:
                writer.writerow(["https://www.iulm.it" + link])
        
        print(f"Extracted {len(links)} links and saved to links.csv")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Example usage
if __name__ == "__main__":
    url = 'https://www.iulm.it/en/offerta-formativa#lauree-triennali'  # Replace with the actual URL
    extract_links(url) 