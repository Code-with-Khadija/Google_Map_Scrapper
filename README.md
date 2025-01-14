# Google Maps Data Scraper

This project provides a Python-based solution for scraping business information from Google Maps, specifically targeting car detailing services. The script uses Selenium for web automation and Requests for extracting additional data, including email addresses, from business websites.

## Features
- **Scroll and Extract:** Scroll through Google Maps listings and extract business data such as name, rating, and website.
- **Email Extraction:** Extract valid email addresses from business websites.
- **CSV Export:** Save the extracted data into a CSV file for easy usage.
- **Error Handling:** Includes robust error handling to manage runtime issues.

## Prerequisites

### Software Requirements
- Python 3.8 or higher
- Google Chrome Browser
- ChromeDriver compatible with your Chrome version

### Python Libraries
Install the required libraries using the following command:
```bash
pip install selenium requests
```

## Setup

### 1. Install ChromeDriver
Download the ChromeDriver that matches your Chrome version from [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/) and add it to your system's PATH.

### 2. Clone the Repository
Clone or download this repository to your local system.

### 3. Script Configuration
No configuration is required. The script includes hardcoded search criteria for car detailing services.

## How It Works

### Main Steps
1. **Initialize Selenium Driver:**
   - Opens Google Maps in a Chrome browser.
   - Searches for "Car Detailing."
2. **Scroll and Extract Data:**
   - Scrolls through the listings.
   - Extracts business names, ratings, and websites.
3. **Email Extraction:**
   - Scrapes email addresses directly from the business websites using HTTP requests.
4. **Save Data:**
   - Saves the extracted data to a CSV file.

### Example Output
CSV file columns:
- Name
- Rating
- Website
- Email

## Usage

1. **Run the Script:**
   Execute the script using Python:
   ```bash
   python script_name.py
   ```

2. **Output:**
   - Extracted data is saved as `car_detailing_data_2.csv` in the current directory.

### Example Console Output:
```plaintext
Processed: ABC Car Detailing, Website: https://example.com
Processed 1/10: ABC Car Detailing - contact@example.com
Successfully processed 10 businesses
Data successfully saved to car_detailing_data_2.csv
```

## Code Overview

### `scroll_and_extract_data(driver)`
- Scrolls through Google Maps listings and extracts:
  - Business name
  - Rating
  - Website

### `extract_emails_from_websites(businesses)`
- Uses regex patterns to scrape email addresses from business websites via HTTP requests.

### `save_to_csv(data, filename)`
- Saves extracted data to a CSV file.

### `initialize_driver()`
- Configures and initializes the Selenium Chrome WebDriver.

## Error Handling
- Handles errors such as missing elements, website access issues, or email extraction failures.
- Logs errors to the console for troubleshooting.

## Limitations
- Requires Google Chrome and ChromeDriver.
- May need adjustments if Google Maps changes its layout or structure.
- Limited to publically accessible information.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it.

## Acknowledgments
- [Selenium](https://www.selenium.dev/) for web automation.
- [Requests](https://docs.python-requests.org/en/latest/) for HTTP requests.
- Google Maps for providing business listings.

