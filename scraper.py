from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Scraper:
        
        time.sleep(2)
        print("Scraper ready")
        driver = webdriver.Firefox()
        URL = "https://www.ethicalsuperstore.com/special-offers/"
        driver.get(URL)
        driver.implicitly_wait(10)

        def __init__(self):
            
            self.cookie_clicker()
        
        def cookie_clicker(self):

            try:
                cookie_button = self.driver.find_element(by=By.ID, value = "onetrust-accept-btn-handler")
                cookie_button.click()
                print("cookies found")
            except:
                print("no cookies")
                pass
        
        

        


@dataclass
class product():
    
    scraper = Scraper()
    
    def product_name(self) -> str:
        """Opens driver and goes to page"""
        product_link =  self.scraper.driver.find_element(by=By.XPATH, value ='/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[3]/div[1]/div[4]/div[1]/article/div/h2/a')
        product_linktext = product_link.text
        return product_linktext

def main():
    product1 = product
    
    print(f"product 1 is called: {product1.product_name(product1)}")

if __name__ == "__main__":
    
    main()