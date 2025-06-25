import scrapy
import csv
import os
import random
from bs4 import BeautifulSoup

class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    
    def start_requests(self):
        # Read links from links.csv
        with open('../links.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with id 'main'
        main_div = soup.find('div', id='main')
        
        if main_div:
            # Extract text and trim
            content = main_div.get_text(strip=True, separator='\n')
            
            # Generate a random number
            random_number = random.randint(1000, 9999)
            
            # Use the course name and random number for the filename
            course_name = self.extract_course_name(soup)
            filename = f"{course_name}_{random_number}.txt"
            
            # Create output directory if it doesn't exist
            os.makedirs('output', exist_ok=True)
            
            # Write the content to a file
            with open(os.path.join('output', filename), 'w', encoding='utf-8') as f:
                f.write(response.url + '\n\n')  # Append the link at the top
                f.write(content)
    
    def extract_course_name(self, soup):
        # Find the title div
        title_div = soup.find('div', class_='title-page__title')
        if title_div:
            return title_div.get_text(strip=True)
        return "course_name"