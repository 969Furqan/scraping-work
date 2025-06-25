import scrapy
import csv
import os
import random
import re
from bs4 import BeautifulSoup

class CourseSpider(scrapy.Spider):
    name = "course_spider"

    def start_requests(self):
        # Read links from links.csv
        with open('../links.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Parse the response using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from the specified tags
        banner_text = soup.find('section', class_='banner', role='main').get_text(strip=True, separator='\n')
        main_content_text = soup.find('div', id='dcProgMainContent', class_='row').get_text(strip=True, separator='\n')

        # Combine the extracted text
        content = f"{response.url}\n\n{banner_text}\n\n{main_content_text}"

        # Generate a filename using the course name and a random number
        course_name = soup.title.string.strip()
        # Remove or replace invalid filename characters
        course_name = re.sub(r'[<>:"/\\|?*]', '_', course_name)
        random_number = random.randint(1000, 9999)
        filename = f"{course_name}_{random_number}.txt"

        # Ensure the output directory exists
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)

        # Save the content to a file
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        self.log(f'Saved file {file_path}')