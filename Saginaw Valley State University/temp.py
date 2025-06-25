import os
import csv
from bs4 import BeautifulSoup

# Input and output file paths
input_file = "gradlinks.txt"  # Path to your input TXT file
output_file = "temp.csv"  # Path to your output CSV file

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Input file {input_file} not found!")
else:
    # Initialize a list to store the href links
    links = []

    # Read and parse the gradlinks.txt file
    with open(input_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].strip()
            links.append(href)

    # Write the links to the CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for link in links:
            writer.writerow([link])

    print(f"Extracted {len(links)} links and saved to {output_file}.")
