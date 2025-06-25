from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

def extract_links(base_url, class_name, output_csv):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    all_links = []
    
    try:
        # Navigate through all pages
        page = 0
        while True:
            # Construct URL with page parameter
            url = f"{base_url}?course_type=All&area_disciplinare=All&access_type=All&lang=All&field_interateneo_value=All&field_name_value=&page={page}"
            
            # Navigate to the URL
            driver.get(url)
            time.sleep(2)  # Small delay to ensure page loads
            
            # Wait for the div to be present (timeout after 20 seconds)
            wait = WebDriverWait(driver, 20)
            try:
                div = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))
                )
                
                # Find all links within the div
                links = div.find_elements(By.TAG_NAME, "a")
                
                # Extract href attributes
                href_list = [link.get_attribute('href') for link in links if link.get_attribute('href')]
                all_links.extend(href_list)
                
                # Check if next page exists
                try:
                    pagination = driver.find_element(By.CLASS_NAME, "pagination")
                    next_button = pagination.find_element(By.CLASS_NAME, "pager__item--next")
                    if not next_button:
                        break
                except:
                    break
                
                page += 1
                
            except TimeoutException:
                break  # If div not found, assume we've reached the end
                
        # Write all collected links to CSV file
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Link'])  # Write header
            for link in all_links:
                writer.writerow([link])
                
        print(f"Links from all pages extracted and saved to {output_csv}")
            
    except WebDriverException as e:
        print(f"WebDriver error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Always close the browser
        driver.quit()

# Example usage
url = 'https://en.unipv.it/en/education/bachelors-and-master-degree-programs/degree-programs'
class_name = 'views-view-grid'
output_csv = 'links.csv'

extract_links(url, class_name, output_csv)