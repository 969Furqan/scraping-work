import csv

input_file = 'links.csv'
output_file = 'unique_links.csv'

# Read the links from the CSV file
with open(input_file, mode='r', newline='') as file:
    reader = csv.reader(file)
    links = list(reader)

# Remove duplicates
unique_links = list(set(link[0] for link in links))

# Write the unique links back to a new CSV file
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    for link in unique_links:
        writer.writerow([link])

print(f"Removed duplicates. Unique links are saved in {output_file}.")