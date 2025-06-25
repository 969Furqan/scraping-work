import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Define the URL of the page to scrape
url = "https://www.isu.edu/eisu/online-programs/"

# Send an HTTP request to the URL
response = requests.get(url)

# If the request is successful, continue scraping
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the div with class 'tab-content' (assuming it contains the links you're interested in)
    tab_content = soup.find("div", class_="tab-content")

    # Find all anchor tags within the tab content
    anchor_tags = tab_content.find_all("a", href=True)

    # Open a CSV file to store the links
    with open("onlineCourse.csv", "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Loop through all anchor tags and process the href links
        for tag in anchor_tags:
            link = tag["href"]
            
            # If the link does not start with "https://www.isu.edu", prepend the base URL
            if not link.startswith("https://www.isu.edu"):
                link = urljoin(url, link)
            
            # Write the link to the CSV file
            csv_writer.writerow([link])

    print("Links have been saved to onlineCourse.csv")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
