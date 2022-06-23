from scraper import Scraper
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import math
import pandas as pd
import uuid
import json
import os

class TestScraper(unittest.TestCase):
    
        scraper = Scraper
        scraper.__init__(scraper)
        driver = webdriver.Firefox()
        URL = "https://www.ethicalsuperstore.com/special-offers/?page=1"
        driver.get(URL)
        driver.implicitly_wait(10)
        driver.maximize_window()
        time.sleep(2)
        print("Scraper ready")
        scraper.cookie_clicker(scraper)
        #driver.quit()
        pass

        def test_find_pages(self):
                
                self.assertEqual(self.scraper.find_pages(self.scraper)[0], "https://www.ethicalsuperstore.com/special-offers/?page=1")
                #self.driver.quit()
                
        def test_find_total_products(self) -> int:
                
                self.assertIsInstance(self.scraper.find_total_products(self.scraper), int)
                #self.driver.quit()
                
        def test_find_products_on_page(self) -> list:
                '''Finds the firefox elements for each product on the current url
                
                Returns:
                self.driver.find_elements_by_class_name("view_product_link"): list of all the products on the page'''
                self.assertEqual(len(self.scraper.find_products_on_page(self.scraper)), 384)
                #self.driver.quit()

        def test_number_of_products_on_page(self) -> int:
                '''Returns how many products there are on the page'''
                test = isinstance(self.scraper.number_of_products_on_page(self.scraper), int)
                self.assertIs(test, True)
                
                #self.driver.quit()

        def test_find_product_names(self) -> list:
                '''Finds the name of the product'''
                self.scraper.driver.get(self.URL)
                names = self.scraper.find_product_names(self.scraper)
                if names and isinstance(names, list):
                        isstring = all(isinstance(i, str) for i in names)
                else:
                        isstring = False
                
                self.assertIs(isstring, True)
                #self.driver.quit()


        def test_time_estimate(self):
                '''Makes an estimate for how much time the program will take to run depending on how long it has already taken.
                
                Args:
                done (int): how many items are completed
                total_to_do (int): how many items are still to be processed
                start_time (float): time the timed programme first started
                
                Returns:
                String with minutes and seconds remaining.'''
                
                test = isinstance(self.scraper.time_estimate(self.scraper, done=0,total_to_do=2,start_time=time.time()), str)
                self.assertIs(test, True)
                #self.driver.quit()

        def product_for_testing(self,number):
                
                
                self.scraper.driver.get(self.URL)
                producturl = self.scraper.get_product_url(self.scraper, self.scraper.find_products_on_page(self.scraper)[number])
                self.scraper.driver.get(producturl)

        def test_get_credentials(self) -> list:
                ''''Gets the ethical credential for each product, returns them as list'''
               #go to a product page
                self.product_for_testing(0)
                test = isinstance(self.scraper.get_credentials(self.scraper)[0], str)
                self.assertIs(test, True)
                #self.driver.quit()


        def test_get_id(self) -> str:
                '''Gets the product id'''
                #go to a product page
                self.product_for_testing(0)
                test = isinstance(self.scraper.get_id(self.scraper), str)
                self.assertIs(test, True)

                #self.driver.quit()



        def test_get_name(self) -> str:
                '''Gets the product name'''
                self.product_for_testing(0)
                test = isinstance(self.scraper.get_name(self.scraper), str)
                self.assertIs(test, True)
                #self.driver.quit()

        def test_get_price(self) -> float:
                '''Gets the product price'''
                self.product_for_testing(0)
                
                test = isinstance(self.scraper.get_price(self.scraper), float)
                self.assertIs(test, True)
                
                #self.driver.quit()
                
        def test_get_reduction(self) -> str:
                '''Gets the level of reduction'''
                self.product_for_testing(0)
                
                test = isinstance(self.scraper.get_reduction(self.scraper), str)
                self.assertIs(test, True)
                #self.driver.quit()
                
        def test_get_category(self) -> str:
                '''Gets the product category'''
                self.product_for_testing(0)
                test = isinstance(self.scraper.get_category(self.scraper), str)
                self.assertIs(test, True)
                #self.driver.quit()
                
        def test_get_url(self) -> str:
                '''gets the url of the current page'''
                self.product_for_testing(0)
                test = isinstance(self.scraper.get_url(self.scraper), str)
                self.assertIs(test, True)
                #self.driver.quit()
                

        def test_return_product_info_dict(self):
                '''makes a list of the various product information'''
                self.product_for_testing(0)
                test = isinstance(self.scraper.return_product_info_dict(self.scraper),dict)
                self.assertIs(test, True)
                #self.driver.quit()

        def test_get_product_url(self):
                self.driver.get(self.URL)
                products_on_page = self.scraper.find_products_on_page(self)
                product = products_on_page[0]
                test = isinstance(self.scraper.get_product_url(self.scraper, product), str)
                self.assertIs(test,True)
                #self.driver.quit()


        def test_updater_get_all_ids(self):
                '''gets the ids of all the sale items'''
                ids = {}
                pages = [self.URL,"https://www.ethicalsuperstore.com/special-offers/?page=2"]
                
                for url in pages:
                        self.driver.get(url)
                        products_on_page = self.scraper.find_products_on_page(self)
                for product in products_on_page:
                        ids[product.get_attribute("data-product-sku")] = [url,self.scraper.get_product_url(self,product)]
                test = isinstance(self.scraper.updater_get_all_ids(self.scraper), dict)
                self.assertIs(test,True)
                #self.driver.quit()


        # def updater_add_info(self, to_add: list, id: int) -> dict:
        #         '''gets all the needed info for items to be added to the spreadsheet'''
                
        #         self.driver.get(to_add[1])
        #         try:
        #         product_info = self.return_product_info_dict(self)
        #         [[key, value]] = product_info.items()
        #         home = os.getcwd()
        #         os.mkdir(f"data/{key}")
        #         os.chdir(f"data/{key}")
        #         with open (f"{key}.json", "w") as outfile:
        #                 json.dump(product_info, outfile)
        #         with open((f'{key}.png'), 'wb') as file:
        #                 file.write(self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div[1]/a/figure/img').screenshot_as_png)
        #         os.chdir(home)
        #         except: 
        #         print("product not found")
        #         product_info = {}
                
        #         return product_info    

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    Scraper.driver.quit()