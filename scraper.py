from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Scraper:
        
        def cookie_clicker(self):

            try:
                cookie_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '"//*[@id="onetrust-accept-btn-handler"')))

             #cookie_button = driver.find_element_by_name(by=By.XPATH, value = '//*[@id="onetrust-accept-btn-handler"]')
                cookie_button.click
                print("cookies found")
            except:
                print("no cookies")
                pass
        
        def open(self):
            
            time.sleep(2)
            print("Scraper ready")
            driver = webdriver.Firefox()
            URL = "https://www.ethicalsuperstore.com/special-offers/"
            driver.get(URL)
            driver.implicitly_wait(10)
            self.cookie_clicker(self)

        


@dataclass
class product():
    scraper = Scraper
    scraper.open(scraper)
    def product_name(self) -> str:
        """Opens driver and goes to page"""
        product_link =  self.scraper.driver.find_element(by=By.XPATH, value ='/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[3]/div[1]/div[4]/div[1]/article/div/h2/a')
        product_linktext = product_link.text
        return product_linktext

def main():
    scraper = Scraper
    product1 = product
    
    print(f"product 1 is called: {product1.product_name(product1)}")

if __name__ == "__main__":
    
    main()