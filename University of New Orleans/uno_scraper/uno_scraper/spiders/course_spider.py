import scrapy
import random
import csv
import os
from bs4 import BeautifulSoup

class CourseSpider(scrapy.Spider):
    name = 'course_spider'
    allowed_domains = ['uno.edu', 'online.uno.edu']
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(CourseSpider, self).__init__(*args, **kwargs)
        # Load the links from the CSV file
        self.load_links()

    def load_links(self):
        """Load links from links.csv"""
        with open('../newlinks.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.start_urls.append(row[0])  # Assuming each row contains a single link

    def parse(self, response):
        """Main parsing method."""
        url = response.url
        content = ""

        # For online.uno.edu links, extract specific sections
        if url.startswith('https://online.uno.edu/'):
            content = self.extract_uno_online_content(response)
        else:
            content = self.extract_paragraph_content(response)

        # If content is found, save it
        if content:
            random_number = random.randint(1000, 9999)
            course_name = url.split('/')[-2]  # Use part of the URL as the course name
            filename = f'output/{course_name}_{random_number}.txt'

            # Save the content to a file
            self.save_to_file(filename, content, url)

    def extract_uno_online_content(self, response):
        """Extract content for https://online.uno.edu/"""
        sections = [
            'overview-section',
            'tuition-section',
            'calendar-section',
            'admission-section',
            'courses-section'
        ]
        content = ""

        for section in sections:
            div = response.css(f'div.{section}')
            if div:
                soup = BeautifulSoup(div.get(), 'html.parser')
                section_content = soup.get_text(strip=True, separator='\n')
                content += f"\n{section.capitalize()}\n"
                content += section_content

        return content

    def extract_paragraph_content(self, response):
        """Extract content for other URLs."""
        div = response.css('div.layout-content')
        if div:
            soup = BeautifulSoup(div.get(), 'html.parser')
            return soup.get_text(strip=True, separator='\n')
        return ""

    def save_to_file(self, filename, content, url):
        """Save the content to a text file with the URL at the top."""
        os.makedirs('output', exist_ok=True)  # Ensure the output directory exists
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"URL: {url}\n\n")  # Write the URL at the top
            file.write(content)
        self.log(f'Saved content to {filename}')
