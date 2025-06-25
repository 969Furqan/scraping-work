import scrapy
import csv
import os
import random
from bs4 import BeautifulSoup

class LinkSpider(scrapy.Spider):
    name = "link_spider"

    def start_requests(self):
        # Read URLs from links.csv
        with open('../links.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                url = row[0]
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Use BeautifulSoup to parse the response
        soup = BeautifulSoup(response.text, 'html.parser')
        content_wrapper = soup.find('div', id='content')

        if content_wrapper:
            # Extract the text, trim, and add newlines
            content = content_wrapper.get_text(strip=True, separator='\n')

            # Get text from div id unit-banner
            banner_div = soup.find('div', id='unit-banner')
            if banner_div:
                banner_text = banner_div.get_text(strip=True)
            else:
                banner_text = "no_banner"

            # Generate a random number for the filename
            random_number = random.randint(1000, 9999)

            # Create the filename using banner text and random number
            filename = f"{banner_text}_{random_number}.txt"

            # Ensure the output directory exists
            os.makedirs('output', exist_ok=True)

            # Write the content to a file
            with open(f'output/{filename}', 'w', encoding='utf-8') as f:
                f.write(f"URL: {response.url}\n\n")
                f.write(content)

            self.log(f'Saved file {filename}')