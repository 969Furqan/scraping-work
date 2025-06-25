import scrapy
import os
import random
import csv
from bs4 import BeautifulSoup

class ContentSpider(scrapy.Spider):
    name = 'content_spider'

    def __init__(self, *args, **kwargs):
        super(ContentSpider, self).__init__(*args, **kwargs)
        self.processed_urls = set()

    # Define the start URLs from the links.csv
    def start_requests(self):
        links_file = "../links.csv"  # Path to your input CSV file

        if not os.path.exists(links_file):
            self.logger.error("links.csv file not found!")
            return

        with open(links_file, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                url = row[0].strip()  # Trim whitespace from the URL
                if url not in self.processed_urls:
                    self.processed_urls.add(url)
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract title from the h1 tag with id acalog-page-title
        title = response.css("h1::text").get(default="course").strip()

        # Extract content inside <tr role="main"> or <main>
        soup = BeautifulSoup(response.text, "html.parser")
        tr_tag = soup.find("tr", role="main")
        main_tag = soup.find("main")

        if tr_tag:
            content = tr_tag.get_text(strip=True, separator="\n")
        elif main_tag:
            content = main_tag.get_text(strip=True, separator="\n")
        else:
            self.logger.warning(f"No content found inside <tr role='main'> or <main> for {response.url}")
            return

        # Generate a filename from the title
        random_suffix = random.randint(1000, 9999)
        sanitized_title = "".join([c if c.isalnum() or c in (' ', '_') else '_' for c in title])
        file_name = f"{sanitized_title.replace(' ', '_')}_{random_suffix}.txt"

        # Create output folder if it doesn't exist
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        # Prepare content to write into the file
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"URL: {response.url}\n\n")
            f.write(content + "\n\n")

        self.logger.info(f"Saved content to {file_path}")
