import scrapy
import csv
import os
import random
from bs4 import BeautifulSoup
import re

class LinkSpider(scrapy.Spider):
    name = "link_spider"

    def start_requests(self):
        # Read URLs from links.csv
        with open('../links.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Use BeautifulSoup to parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('div', class_='body-wrapper')

        if main_content:
            # Trim and clean the text
            content_text = main_content.get_text(strip=True, separator='\n')

            # Generate a random number for the filename
            random_number = random.randint(1000, 9999)

            # Extract a course name or use a placeholder if not available
            course_name = self.extract_course_name(soup) or "course"
            
            # Clean the filename by removing invalid characters
            clean_name = re.sub(r'[<>:"/\\|?*]', '', course_name)
            
            # Create a filename
            filename = f"{clean_name}_{random_number}.txt"

            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)

            # Write the content to a file
            with open(os.path.join('output', filename), 'w', encoding='utf-8') as f:
                f.write(f"URL: {response.url}\n\n")
                f.write(content_text)

    def extract_course_name(self, soup):
        # Implement logic to extract course name, e.g., from a specific tag
        # This is a placeholder implementation
        return soup.title.string if soup.title else None