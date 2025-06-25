import scrapy
import csv
import random
from bs4 import BeautifulSoup
import os

class CourseSpider(scrapy.Spider):
    name = "course_spider"
    
    # Start URLs are read from the 'degreelinks.csv' file
    def start_requests(self):
        with open('../links.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    link = row[0]
                    yield scrapy.Request(url=link, callback=self.parse, meta={'url': link})

    def parse(self, response):
        # Get the main tag content
        main_tag = response.xpath('//main').get()

        # If main tag exists, process it
        if main_tag:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(main_tag, 'html.parser')
            main_text = soup.get_text(strip=True, separator='\n')

            # Extract the course name (assume it's in <h1>, <title>, or similar)
            course_name = response.xpath('//h1/text()').get() or response.xpath('//title/text()').get()

            # Clean up the course name to be a valid file name
            course_name = course_name.strip().replace(' ', '_').replace('/', '_').replace('\\', '_')

            # Add a random number to the filename
            random_number = random.randint(1000, 9999)
            filename = f"{course_name}_{random_number}.txt"

            # Create the output folder if it doesn't exist
            output_dir = "txts"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Write the course URL and content to the file
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write the URL at the top
                f.write(f"Link: {response.meta['url']}\n")
                # Write the cleaned main content
                f.write(main_text.strip())

            self.log(f"Saved file {filename}")

