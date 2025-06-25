import csv
import requests
from bs4 import BeautifulSoup
import random

# Function to extract text from the specified div
def extract_text_from_div(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_='elementor-column elementor-col-100 elementor-top-column elementor-element elementor-element-7f6ea15a')
    if div:
        return div.get_text(strip=True)
    return None

# Read links from CSV
with open('newlinks.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    links = [row[0] for row in reader]

# Extract text and store in a txt file
texts = []
for link in links:
    text = extract_text_from_div(link)
    if text:
        texts.append(text)

# Generate a random 4-digit number for the filename
random_number = random.randint(1000, 9999)
filename = f'extracted_text_{random_number}.txt'

# Write the extracted text to the file
with open(filename, 'w') as file:
    for text in texts:
        file.write(text + '\n')

print(f'Text extracted and saved to {filename}')