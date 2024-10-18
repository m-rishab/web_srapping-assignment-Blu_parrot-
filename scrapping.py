import time
import random
import json
import logging
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Simple logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class OtipyScraper:
    def __init__(self):
        self.url = "https://www.otipy.com/category/vegetables-1"
        self.products = []
    
    def start_browser(self):
        # Setup Firefox in headless mode
        options = Options()
        options.add_argument('--headless')
        return webdriver.Firefox(options=options)
    
    def wait_for(self, driver, selector, seconds=30):
        return WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    
    def scroll_page(self, driver):
        # Scroll with random delays to seem more human-like
        current_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(1.0, 2.0))
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == current_height:
                break
            current_height = new_height
    
    def clean_text(self, text):
        # Remove rupee symbol and units like /kg, /Pack
        text = text.replace('₹', '').strip()
        return re.sub(r'\s*(/kg|/pack|/pc|/pcs|/g)?', '', text, flags=re.I)
    
    def get_product_info(self, card):
        try:
            # Find all the product details
            name = card.find_elements(By.CSS_SELECTOR, '.style_prod_name__QllSp')
            price = card.find_elements(By.CSS_SELECTOR, '.style_selling_price__GaIsF')
            mrp = card.find_elements(By.CSS_SELECTOR, '.style_striked_price__4ghn5')
            qty = card.find_elements(By.CSS_SELECTOR, '.style_prod_qt__cXcqe')
            
            return {
                "Name": name[0].text if name else "N/A",
                "Standard Price": self.clean_text(price[0].text) if price else "N/A",
                "Selling Price": self.clean_text(price[0].text) if price else "N/A",
                "MRP": self.clean_text(mrp[0].text) if mrp else "N/A",
                "Quantity": qty[0].text if qty else "N/A"
            }
            
        except Exception as e:
            logging.error(f"Couldn't get product info: {str(e)}")
            return None
    
    def scrape(self, max_tries=3):
        for attempt in range(max_tries):
            driver = self.start_browser()
            try:
                logging.info(f"Try #{attempt + 1}: Loading page...")
                driver.get(self.url)
                
                # Wait for products to show up
                self.wait_for(driver, '.style_card__v4i84')
                
                previous_product_count = 0
                no_new_products_count = 0
                
                while True:
                    logging.info(f"Got {len(self.products)} products so far...")
                    
                    # Scroll down to load more products
                    self.scroll_page(driver)
                    time.sleep(random.uniform(1.5, 2.5))
                    
                    # Get all product cards
                    cards = driver.find_elements(By.CSS_SELECTOR, '.style_card__v4i84')
                    
                    # Process each card
                    for card in cards:
                        product = self.get_product_info(card)
                        if product and product not in self.products:
                            self.products.append(product)
                    
                    # Check if we got any new products
                    if len(self.products) == previous_product_count:
                        no_new_products_count += 1
                        # If we haven't found new products in 3 consecutive checks, assume we're done
                        if no_new_products_count >= 3:
                            logging.info("No more products found after multiple checks")
                            break
                    else:
                        no_new_products_count = 0
                    
                    previous_product_count = len(self.products)
                
                if self.products:
                    logging.info(f"Successfully scraped {len(self.products)} products")
                    return self.products
                
            except TimeoutException:
                logging.error(f"Page took too long to load (attempt {attempt + 1})")
            except Exception as e:
                logging.error(f"Something went wrong: {str(e)}")
            finally:
                driver.quit()
        
        logging.error("Failed to scrape after all attempts")
        return []
    
    def save_products(self, filename='products.json'):
        if not self.products:
            logging.info("No products to save")
            return
            
        with open(filename, 'w') as f:
            json.dump(self.products, f, indent=4)
        logging.info(f"Saved {len(self.products)} products to {filename}")

def main():
    # Create scraper and run it
    scraper = OtipyScraper()
    scraper.scrape()
    scraper.save_products()

if __name__ == "__main__":
    main()