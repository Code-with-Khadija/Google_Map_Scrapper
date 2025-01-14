from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import re

def scroll_and_extract_data(driver):
    """Scroll and extract data simultaneously"""
    print("Starting scroll and data extraction...")
    businesses = []
    processed_names = set()  # To avoid duplicates
    
    try:
        # Wait for the feed container
        wait = WebDriverWait(driver, 10)
        feed = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']")))
        
        # Initial height
        last_height = driver.execute_script("return arguments[0].scrollHeight", feed)
        
        while True:
            # Extract data from current view
            listings = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK.tH5CWc.THOPZb")
            
            for listing in listings:
                try:
                    # Extract basic info without clicking
                    name = listing.find_element(By.CSS_SELECTOR, "div.qBF1Pd").text.strip()
                    
                    # Skip if already processed
                    if name in processed_names:
                        continue
                    
                    business_info = {
                        'name': name,
                        'rating': 'N/A',
                        'website': 'N/A',
                        'email': 'N/A'
                    }
                    
                    # Try to get rating
                    try:
                        rating = listing.find_element(By.CSS_SELECTOR, "span.MW4etd").text
                        business_info['rating'] = rating
                    except:
                        pass
                    
                    # Try to get website directly from the card
                    try:
                        website_element = listing.find_element(By.CSS_SELECTOR, "a.lcr4fd.S9kvJb")
                        website = website_element.get_attribute("href")
                        if website and not website.startswith("tel:"):
                            business_info['website'] = website
                    except:
                        pass
                    
                    businesses.append(business_info)
                    processed_names.add(name)
                    print(f"Processed: {name}, Website: {business_info['website']}")
                    
                except Exception as e:
                    print(f"Error processing listing: {str(e)}")
                    continue
            
            # Scroll feed
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", feed)
            time.sleep(2)

            
            # Calculate new scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", feed)
            
            if new_height == last_height:
                # Check if we've reached the bottom
                break
                
            last_height = new_height
            
        print(f"Found {len(businesses)} unique businesses")
        return businesses
        
    except Exception as e:
        print(f"Error during scroll and extract: {str(e)}")
        return businesses

def save_to_csv(data, filename):
    """Save the extracted data to CSV"""
    if data:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'rating', 'website', 'email'])
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully saved to {filename}")
    else:
        print("No data found to save.")

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)

def extract_emails_from_websites(businesses):
    """Extract emails from websites using requests without opening browser"""
    print("\nStarting email extraction from websites...")
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i, business in enumerate(businesses, 1):
        if business['website'] != 'N/A':
            try:
                # Get website content using requests
                response = requests.get(
                    business['website'], 
                    headers=headers, 
                    timeout=10,
                    verify=False
                )
                page_source = response.text
                
                # Extract email from page source
                emails = re.findall(email_pattern, page_source)
                
                # Filter valid emails
                valid_emails = [
                    email for email in emails 
                    if '@' in email 
                    and '.' in email.split('@')[1]
                    and not email.startswith('.')
                    and not email.endswith('.')
                ]
                
                business['email'] = valid_emails[0] if valid_emails else 'N/A'
                print(f"Processed {i}/{len(businesses)}: {business['name']} - {business['email']}")
                
            except Exception as e:
                print(f"Error processing website {business['website']}: {str(e)}")
                business['email'] = 'N/A'
    
    return businesses

def main():
    driver = initialize_driver()
    try:
        # Navigate to Google Maps
        driver.get("https://www.google.com/maps")
        wait = WebDriverWait(driver, 10)
        
        # Search for car detailing
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.send_keys("Car Detailing")
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)
        
        # First phase: Scroll and extract basic data
        businesses = scroll_and_extract_data(driver)
        
        # Close the driver as we don't need it anymore
        #driver.quit()
        
        # Second phase: Extract emails from websites using requests
        if businesses:
            businesses = extract_emails_from_websites(businesses)
            print('businesses: ', businesses)
            save_to_csv(businesses, "car_detailing_data_2.csv")
            print(f"Successfully processed {len(businesses)} businesses")
        else:
            print("No data was collected")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
