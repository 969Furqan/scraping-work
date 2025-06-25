import scrapy
import csv
import os
import random
from bs4 import BeautifulSoup

class CoursesSpider(scrapy.Spider):
    name = "courses"
    
    def start_requests(self):
        # Read URLs from links.csv in parent directory
        try:
            with open('../links.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    yield scrapy.Request(url=row[0], callback=self.parse)
        except FileNotFoundError:
            self.logger.error("links.csv file not found in parent directory")
            return

    def parse(self, response):
        # Extract content from the div with data-swiftype-name="body"
        body_content = response.css('div[data-swiftype-name="body"]').get()
        
        # Use BeautifulSoup to extract text from the body div
        soup = BeautifulSoup(body_content, 'html.parser')
        body_text = soup.get_text(strip=True, separator='\n')
        
        # Extract course name from the URL
        course_name = response.url.split('/')[-1]
        
        # Generate a random number for the filename
        random_number = random.randint(1000, 9999)
        
        # Create the filename
        filename = f"{course_name}_{random_number}.txt"
        
        # Ensure the output directory exists
        os.makedirs('output', exist_ok=True)
        
        # Write the content to a file
        with open(f'output/{filename}', 'w', encoding='utf-8') as f:
            f.write(f"URL: {response.url}\n\n")
            f.write(body_text)
        
        self.log(f'Saved file {filename}')