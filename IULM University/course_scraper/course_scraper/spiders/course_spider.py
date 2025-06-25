import scrapy
import csv
import os
import requests
from bs4 import BeautifulSoup
import random

class CourseSpider(scrapy.Spider):
    name = "course_spider"

    def start_requests(self):
        # Read links from the CSV file
        with open('../links.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Use requests and BeautifulSoup to parse the page
        page = requests.get(response.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find the <ul> with the specified class
        ul = soup.find('ul', class_='menu-scroll')
        
        # Extract all <a> tags within the <ul>
        links = []
        if ul:
            a_tags = ul.find_all('a')
            for a in a_tags:
                href = a.get('href')
                if href and href != '#':  # Skip empty links and hash-only links
                    # Construct full URL
                    full_url = "https://www.iulm.it" + href if href.startswith('/') else href
                    links.append(full_url)

        # Generate random number for filename
        random_number = random.randint(1000, 9999)
        course_name = response.url.split('/')[-2]
        filename = f"{course_name}_{random_number}.txt"

        # Ensure output directory exists
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        # Write content to file
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as file:
            file.write(f"URL: {response.url}\n\n")
            
            # First write main content
            main_content = soup.find('main')
            if main_content:
                text_content = main_content.get_text(separator='\n', strip=True)
                file.write(text_content + "\n\n")

            # Then write content from each linked page
            for link in links:
                page_response = requests.get(link)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    section = page_soup.find('section', class_='content-single')
                    if section:
                        text_content = section.get_text(separator='\n', strip=True)
                        file.write(text_content + "\n\n")

        self.log(f'Saved file {filename}')