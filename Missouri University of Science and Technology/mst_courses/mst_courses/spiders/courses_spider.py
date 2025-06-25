import scrapy
from bs4 import BeautifulSoup
import csv
import random
import os
from pathlib import Path

class CoursesSpider(scrapy.Spider):
    name = 'courses'
    
    def start_requests(self):
        # Create output directory if it doesn't exist
        Path('output').mkdir(exist_ok=True)
        
        # Read links from CSV
        with open('../links.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                url = row[0].strip()
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Get main content using BS4
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('main')
        
        if main_content:
            # Get text content
            text_content = main_content.get_text(separator='\n', strip=True)
            
            # Get course name from title or h1
            title = soup.find('h1')
            if title:
                course_name = title.get_text(strip=True)
            else:
                course_name = "course"
                
            # Clean filename
            clean_name = "".join(c for c in course_name if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_name = clean_name.replace(' ', '_')
            
            
            # Add random number and create filename
            random_num = random.randint(1000, 9999)
            filename = f"output/{clean_name}_{random_num}.txt"
            
            # Write content to file
            with open(filename, 'w', encoding='utf-8') as f:
                # Write URL at the top
                f.write(f"Source: {response.url}\n\n")
                # Write main content
                f.write(text_content)
            
            self.log(f'Saved file {filename}') 