import scrapy
import random
import csv
import os
from bs4 import BeautifulSoup

class CourseSpider(scrapy.Spider):
    name = 'course_spider'
    allowed_domains = ['jwu.edu', 'online.jwu.edu', 'catalog.jwu.edu']
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(CourseSpider, self).__init__(*args, **kwargs)
        # Load the links from the CSV file
        self.load_links()

    def load_links(self):
        """Load links from links.csv"""
        with open('../links.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.start_urls.append(row[0])  # Assuming each row contains a single link

    def parse(self, response):
        # Get the URL of the page
        url = response.url

        # Initialize content variable
        content = ""

        # Depending on the URL, extract content
        if url.startswith('https://online.jwu.edu/'):
            content = self.extract_online_content(response)
        elif url.startswith('https://www.jwu.edu/'):
            content = self.extract_jwu_content(response)
        elif url.startswith('https://catalog.jwu.edu/'):
            content = self.extract_catalog_content(response)

        if content:
            # Create a random number for the filename
            random_number = random.randint(1000, 9999)
            course_name = url.split('/')[-2]  # Use part of the URL as the course name
            filename = f'output/{course_name}_{random_number}.txt'

            # Write the content to a file
            self.save_to_file(filename, content, url)

    def extract_online_content(self, response):
        """Extract content for https://online.jwu.edu/"""
        div = response.css('div#program-overview')
        if div:
            soup = BeautifulSoup(div.get(), 'html.parser')
            return soup.get_text(strip=True, separator='\n')  # Use get_text directly
        return ""

    def extract_jwu_content(self, response):
        """Extract content for https://www.jwu.edu/"""
        div = response.css('div.canvas')
        if div:
            soup = BeautifulSoup(div.get(), 'html.parser')
            return soup.get_text(strip=True, separator='\n')  # Use get_text directly
        return ""

    def extract_catalog_content(self, response):
        """Extract content for https://catalog.jwu.edu/"""
        div = response.css('div#content-wrapper')
        if div:
            soup = BeautifulSoup(div.get(), 'html.parser')
            return soup.get_text(strip=True, separator='\n')  # Use get_text directly
        return ""

    def save_to_file(self, filename, content, url):
        """Save the content to a text file with the URL at the top"""
        os.makedirs('output', exist_ok=True)  # Ensure the output directory exists
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"URL: {url}\n\n")  # Write the URL at the top
            file.write(content)
        self.log(f'Saved content to {filename}')
