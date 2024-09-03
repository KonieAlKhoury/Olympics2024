import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

def main():
    # URL for the olympic medal table
    MEDALS_URL = 'https://olympics.com/en/paris-2024/medals'

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Specify the path to the ChromeDriver executable
    chrome_driver_path = '/usr/local/bin/chromedriver'  # Update this path if necessary
    
    # Initialize the WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("Navigating to the page...")
        start_time = time.time()
        driver.get(MEDALS_URL)
        end_time = time.time()
        print(f"Page loaded in {end_time - start_time:.2f} seconds")

        # Get the page title
        title = driver.title
        print(f"Page Title: {title}")

        # Initialize an empty dictionary to store the data
        data_dict = {}  

        # Get scroll height ans scralling intervals
        last_height = driver.execute_script("return document.body.scrollHeight")
        Scroll_interval = round(last_height/10)


        # Scroll down to bottom with an internal of 1/10 of the page height
        for i in range(0, last_height, Scroll_interval):
            driver.execute_script("window.scrollTo(0, {});".format(i))
            time.sleep(0.5)
        
            # Get the page source
            page_source = driver.page_source
    
            # Parse the page source using BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract data using data-testid
            noc_rows = soup.find_all('div', {'data-testid': 'noc-row'})
            for row in noc_rows:
                try:
                    country_code = row.find('span', class_='euzfwma4 emotion-srm-5xu01z').text
                    country_name = row.find('span', class_='euzfwma5 emotion-srm-uu3d5n').text
                    gold = row.find_all('span', class_='e1oix8v91 emotion-srm-19huvme')[0].text
                    silver = row.find_all('span', class_='e1oix8v91 emotion-srm-19huvme')[1].text
                    bronze = row.find_all('span', class_='e1oix8v91 emotion-srm-19huvme')[2].text
                    total = row.find('span', class_='e1oix8v91 emotion-srm-bnzwbp').text
                    
                    # Use country code as the key to ensure uniqueness
                    data_dict[country_code] = [country_name, country_code, gold, silver, bronze, total]

                except AttributeError as e:
                    print(f"Error extracting data from row: {e}")

        # Convert the dictionary values to a list
        data = list(data_dict.values())
        df = pd.DataFrame(data, columns=['Country', 'Country Code', 'Gold', 'Silver', 'Bronze', 'Total'])
        
        df.to_csv('medals.csv', index=False)
        print("Data saved to medals.csv")

    except Exception as e:
        print(f"Error fetching the page: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()