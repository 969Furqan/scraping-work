import scrapy
import os
import random
from bs4 import BeautifulSoup

class CourseSpider(scrapy.Spider):
    name = "course_spider"

    def start_requests(self):
        # Read URLs from links.csv
        with open('../links.csv', 'r') as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()  # Trim whitespace
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Use BeautifulSoup to parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('main')

        if main_content:
            # Extract the course name from the URL
            course_name = response.url.split('/')[-1].split('?')[0]
            # Generate a random number for the filename
            random_number = random.randint(1000, 9999)
            # Create the filename
            filename = f"{course_name}_{random_number}.txt"
            # Create the output directory if it doesn't exist
            os.makedirs('output', exist_ok=True)
            # Write the content to a file
            with open(os.path.join('output', filename), 'w', encoding='utf-8') as f:
                f.write(response.url + '\n\n')  # Append the URL at the top
                f.write(main_content.get_text(strip=True, separator='\n'))  # Trim and newline separator

            self.log(f'Saved file {filename}') 