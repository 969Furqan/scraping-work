import scrapy
import csv
import os
import random
import re
from bs4 import BeautifulSoup

class CanadoreSpider(scrapy.Spider):
    name = "canadore"
    handle_httpstatus_list = [404]  # Allow 404 responses to be processed
    
    def start_requests(self):
        # Read links from the CSV file
        with open('../links.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Skip processing if page returns 404
        if response.status == 404:
            self.logger.info(f"Skipping 404 page: {response.url}")
            return
            
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        main_div = soup.find('div', class_='col-xs-12', role='main')
        
        if main_div:
            # Extract the course name and clean it
            course_name = main_div.find('h1').get_text(strip=True) if main_div.find('h1') else 'course'
            # Remove or replace invalid filename characters
            course_name = re.sub(r'[<>:"/\\|?*]', '-', course_name)
            
            # Generate a random number for the filename
            random_number = random.randint(1000, 9999)
            filename = f"{course_name}_{random_number}.txt"
            
            # Prepare the content
            content = main_div.get_text(separator='\n', strip=True)
            content = f"{response.url}\n\n{content}"
            
            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)
            
            try:
                # Write the content to a file
                with open(os.path.join('output', filename), 'w', encoding='utf-8') as f:
                    f.write(content)
            except OSError as e:
                self.logger.error(f"Failed to write file {filename}: {str(e)}")