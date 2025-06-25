from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def main():
    # Initialize Chrome driver (without headless mode)
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    urls = [
        'https://futurestudents.mst.edu/academic-programs/undergraduate-programs/',
        'https://futurestudents.mst.edu/academic-programs/graduate-programs/'
    ]
    
    all_links = []
    
    try:
        for url in urls:
            # Get page
            driver.get(url)
            print(f"\nProcessing: {url}")
            
            # Wait for links to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mst-program-link"))
            )
            
            # Get all links
            links = driver.find_elements(By.CLASS_NAME, "mst-program-link")
            page_links = [link.get_attribute('href') for link in links]
            all_links.extend(page_links)
            
            print(f"Found {len(page_links)} links")
            time.sleep(2)  # Pause so you can see the page
        
        # Write links to CSV file
        with open('links.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for link in all_links:
                writer.writerow([link])
        
        print(f"\nTotal links extracted to links.csv: {len(all_links)}")
        time.sleep(3)  # Keep browser open briefly
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main() 