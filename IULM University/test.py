import requests
from bs4 import BeautifulSoup

def extract_text_from_links(base_url):
    # Send a GET request to the base URL
    response = requests.get(base_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the <ul> with the specified class
        ul = soup.find('ul', class_='menu-scroll')
        
        # Extract all <a> tags within the <ul>
        links = []
        if ul:
            a_tags = ul.find_all('a')
            for a in a_tags:
                href = a.get('href')
                if href and href != '#':  # Skip empty links and hash-only links
                    # Construct full URL
                    full_url = "https://www.iulm.it" + href if href.startswith('/') else href
                    links.append(full_url)
        
        # Open a text file to write the extracted content
        with open('extracted_content.txt', 'w', encoding='utf-8') as file:
            for link in links:
                # Fetch each linked page
                page_response = requests.get(link)
                if page_response.status_code == 200:
                    page_soup = BeautifulSoup(page_response.content, 'html.parser')
                    
                    # Find the section with class 'content-single'
                    section = page_soup.find('section', class_='content-single')
                    if section:
                        # Extract and write the text content
                        text_content = section.get_text(separator='\n', strip=True)
                        file.write(f"Content from {link}:\n{text_content}\n\n")
                else:
                    print(f"Failed to retrieve the page at {link}. Status code: {page_response.status_code}")
        
        print("Content extraction complete. Check 'extracted_content.txt' for results.")
    else:
        print(f"Failed to retrieve the base page. Status code: {response.status_code}")

# Example usage
if __name__ == "__main__":
    base_url = 'https://www.iulm.it/en/offerta-formativa/corsi-di-lauree-triennali/Lingue-cultura-e-comunicazione-digitale/'
    extract_text_from_links(base_url) 