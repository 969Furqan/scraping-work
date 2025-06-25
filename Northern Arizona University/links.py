import subprocess
import json
import csv
import time

try:
    from seleniumwire import webdriver  # Import from selenium-wire to capture network requests
except ImportError:
    subprocess.check_call(["pip", "install", "selenium-wire"])
    from seleniumwire import webdriver

try:
    from selenium.webdriver.common.by import By
except ImportError:
    subprocess.check_call(["pip", "install", "selenium"])
    from selenium.webdriver.common.by import By

try:
    import blinker
except ImportError:
    subprocess.check_call(["pip", "install", "blinker"])

# Setup Selenium WebDriver (e.g., Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode for efficiency
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

try:
    driver = webdriver.Chrome(seleniumwire_options={}, options=options)
except Exception as e:
    print(f"Error initializing webdriver: {e}")
    raise

# URL to scrape
url = "https://degree-search.nau.edu/search/?ac=ugrd&dm=INPER,ONLIN"

try:
    # Navigate to the URL
    driver.get(url)

    # Allow the page to load completely
    time.sleep(3)  # Adjust sleep time as necessary

    # Find all divs with class "listSegment" inside the div with id "resultList"
    result_list_div = driver.find_element(By.ID, "resultList")
    list_segments = result_list_div.find_elements(By.CLASS_NAME, "listSegment")

    # Interact with each div to trigger the API request
    for segment in list_segments:
        segment.click()  # Click each segment to trigger the API request
        time.sleep(1)  # Wait for the API request to process

    # Extract network requests containing the payload
    extracted_data = []
    for request in driver.requests:
        try:
            if request.response and request.body:
                body = request.body.decode("utf-8", errors="ignore")
                if "ai.operation.name" in body:
                    payload = json.loads(body)
                    operation_name = payload.get("ai.operation.name")
                    if operation_name:
                        extracted_data.append(operation_name)
        except Exception as e:
            print(f"Error processing request: {e}")

    # Save the extracted data to a CSV file
    output_file = "links.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for data in extracted_data:
            writer.writerow([data])

    print(f"Extracted {len(extracted_data)} ai.operation.name entries and saved to {output_file}")

finally:
    # Close the WebDriver
    driver.quit()
