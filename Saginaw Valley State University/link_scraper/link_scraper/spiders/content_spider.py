import scrapy
import os
import random
import csv
from bs4 import BeautifulSoup

class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def start_requests(self):
        links_file = "../links.csv"

        if not os.path.exists(links_file):
            self.logger.error("links.csv file not found!")
            return

        with open(links_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                url = row[0].strip()
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract title from the h1 tag with id acalog-page-title
        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "course"

        # Extract content inside <main> tag
        soup = BeautifulSoup(response.text, "html.parser")
        main_tag = soup.find("div", id= "main")
        main_content = main_tag.get_text(strip=True, separator="\n") if main_tag else "No content found."

        # Generate a filename from the title
        random_suffix = random.randint(1000, 9999)
        file_name = f"{title.replace(' ', '_')}_{random_suffix}.txt"

        # Create output folder if it doesn't exist
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        # Prepare content to write into the file
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"URL: {response.url}\n\n")
            f.write(main_content + "\n\n")

        self.logger.info(f"Saved content to {file_path}")
