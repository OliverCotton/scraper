from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import math
import pandas as pd
import uuid
import json
import os
import boto3
import psycopg2

import urllib3

class Scraper:
        '''Object which scrapes information on salee items from ethical superstore'''

        

        def __init__(self):
            
            self.driver = webdriver.Firefox()
            URL = "https://www.ethicalsuperstore.com/special-offers/?page=1"
            self.driver.get(URL)
            self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            time.sleep(2)
            print("Scraper ready")
            self.cookie_clicker(self)
            
            

        def cookie_clicker(self) -> None:
            '''Looks for the cookies button and clicks it.'''
            try:
                cookie_button = self.driver.find_element(by=By.ID, value = "onetrust-accept-btn-handler")
                cookie_button.click()
                print("cookies found")
            except:
                print("no cookies")
                pass
        
        def find_pages(self) -> list:
            '''Generates list of urls for all the special offers pages
            
            Returns:
                pages: a list of the pages'''

            URL = "https://www.ethicalsuperstore.com/special-offers/?page=1"
            self.driver.get(URL)
            
            select = Select(self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[3]/div[1]/div[3]/div/div/div[3]/select'))
            select.select_by_visible_text('Show 192 items')

            number_of_pages = math.ceil(int(self.find_total_products(self))/192)
            pages = [f"https://www.ethicalsuperstore.com/special-offers/?page={x}" for x in range(1,number_of_pages+1)]
            return pages

        def find_total_products(self) -> int:
            '''Returns the total number of products on offer at any one time
            
            Returns:
            number_of_items_on_sale_elem.text: the total number of current sale items'''
            number_of_items_on_sale_elem = self.driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[3]/div[1]/div[3]/p/b[2]')
            return int(number_of_items_on_sale_elem.text)


        def find_products_on_page(self) -> list:
            '''Finds the firefox elements for each product on the current url
            
            Returns:
            self.driver.find_elements_by_class_name("view_product_link"): list of all the products on the page'''
            return self.driver.find_elements_by_class_name("view_product_link")
        
        def number_of_products_on_page(self) -> int:
            '''Returns how many products there are on the page'''
            return len(self.find_products_on_page(self))
        
        def find_product_names(self) -> list:
            '''Finds the name of the product'''
            product_names = [x.get_attribute("data-product-name") for x in self.find_products_on_page(self)]
            return product_names

        def time_estimate(self, done, total_to_do, start_time):
            '''Makes an estimate for how much time the program will take to run depending on how long it has already taken.
            
            Args:
                done (int): how many items are completed
                total_to_do (int): how many items are still to be processed
                start_time (float): time the timed programme first started
                
            Returns:
                String with minutes and seconds remaining.'''
            to_do = total_to_do - done
            time_per_item = (time.time() - start_time)/(done+0.0001)
            time_to_go = time_per_item * (to_do)
            
            mins = int(time_to_go/60)
            s = int(time_to_go%60)
            return (f"{mins} minutes, {s} seconds")



        def get_credentials(self) -> list:
            ''''Gets the ethical credential for each product, returns them as list'''
            try:
                credential_box_elem = self.driver.find_element_by_class_name("product-ethics-tags")
                credential_elems = credential_box_elem.find_elements_by_xpath("*")
                credentials = [x.get_attribute("title") for x in credential_elems]
            except:
                credentials = []
                pass
            return credentials

        def get_id(self) -> int:
            '''Gets the product id'''
            try:
                id_obj = self.driver.find_element(by=By.CLASS_NAME, value='f-left')
                id_text = id_obj.text
                id = "".join(x for x in id_text if x.isdecimal())
                int(id)
            except:
                print("ID not found")
                id = "NULL"
            return id
        
        def get_name(self) -> str:
            '''Gets the product name'''
            name_obj = self.driver.find_element(by=By.CLASS_NAME, value='product-details__title')
            name = name_obj.text
            return name
        
        def get_price(self) -> float:
            '''Gets the product price'''
            price_elem = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/span[2]")
            price = price_elem.text
            return float(price)
        
        def get_reduction(self) -> str:
            '''Gets the level of reduction'''
            reduction_elem = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div[3]")
            reduction_text = reduction_elem.text
            reduction = reduction_text[-4:-1]
            return (f"{reduction}%")

        def get_category(self) -> str:
            '''Gets the product category'''
            category_elem = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[1]/nav/h3")
            category_text = category_elem.text
            category = category_text[7:]
            return category
        
        def get_url(self) -> str:
            '''gets the url of the current page'''
            url = self.driver.current_url
            return url


        def return_product_info_dict(self):
            '''makes a list of the various product information'''
            dict_entry = {str(uuid.uuid4()):[self.get_id(self),self.get_name(self),self.get_credentials(self), 
                            self.get_price(self), self.get_reduction(self),
                            self.get_category(self), self.get_url(self)]}
            return dict_entry
        
        def get_product_url(self,product):
            url= product.get_attribute("href")
            return url
        
        def updater_get_all_ids(self):
            '''gets the ids of all the sale items'''
            ids = {}
            pages = self.find_pages(self)
            
            for url in pages:
                self.driver.get(url)
                products_on_page = self.find_products_on_page(self)
                for product in products_on_page:
                    ids[product.get_attribute("data-product-sku")] = [url,self.get_product_url(self,product)]
            return ids
        
        def updater_add_info(self, to_add: list, id: int) -> dict:
            '''gets all the needed info for items to be added to the spreadsheet'''
            
            self.driver.get(to_add[1])
            # try:
            product_info = self.return_product_info_dict(self)
            [[key, value]] = product_info.items()
            s3_client = boto3.client('s3')
            s3 = boto3.resource('s3')
            name = value[1].strip()
            #my_bucket = s3.Bucket('ethcialsuperstorescraperbucket')
            
            product_df = pd.DataFrame.from_dict(product_info, orient='index', columns=['ID','Name','Credentials','Price','Reduction', 'Category', 'url'])
            print("trying to connect to db...")
            engine = psycopg2.connect(
                database="db-AKC4DV7UHQYYLURHHNSVDPO2BQ",
                user="postgres",
                password="postgres1",
                host="productinfodb.cpelwh8ugsrt.us-east-1.rds.amazonaws.com",
                port='5432')
            product_df.to_sql('product', engine, scheme='public', if_exists = 'append', index = False)
            print("connected!")
            home = os.getcwd()
            os.mkdir(f"data/{key}")
            os.chdir(f"data/{key}")
            with open (f"{key}.json", "w") as outfile:
                json.dump(product_info, outfile)
                #s3_client.upload_file((f"{key}.json"), 'ethcialsuperstorescraperbucket', (f"{name}.json"))
                s3object = s3.Object('ethcialsuperstorescraperbucket', (f"{name}.json"))
                s3object.put(Body=(bytes(json.dumps(product_info).encode('UTF-8'))))
                
                
            with open((f'{key}.png'), 'wb') as file:
                image = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div[1]/a/figure/img').screenshot_as_png
                file.write(image)
                s3_client.upload_file((f"{key}.png"), 'ethcialsuperstorescraperbucket', (f"{name}.png"))
            
            os.chdir(home)
                # home = os.getcwd()
                # os.mkdir(f"data/{key}")
                # os.chdir(f"data/{key}")
                # with open (f"{key}.json", "w") as outfile:
                #     json.dump(product_info, outfile)
                # with open((f'{key}.png'), 'wb') as file:
                #     file.write(self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div/div[1]/a/figure/img').screenshot_as_png)
                # os.chdir(home)
            # except: 
            #     print("product not found")
            #     product_info = {}
            
            return product_info



def initial_scrape():
    '''Produces a spreadsheet containing all the products on sale.'''
    start = time.time()
    scraper = Scraper
    scraper.__init__(scraper)
    all_ids = scraper.updater_get_all_ids(scraper)
    data = {}
    done = 0
    for i in all_ids:
            
            info = scraper.updater_add_info(scraper,all_ids[i], i)
            [[key, value]] = info.items()
            data[key] = value
            done += 1
            print(f"{done}/{len(all_ids)}. Estimated time remaining: {scraper.time_estimate(scraper, done, len(all_ids), start)}") 
    finish = time.time()-start
    print(finish)

def update():
    '''Updates the "sale_items" spreadsheet'''
    start = time.time()
    spreadsheet = pd.read_excel('sale_items.xlsx', index_col=0)
    scraper = Scraper
    scraper.__init__(scraper)
    sheet_ids = spreadsheet['id'].tolist()
    all_ids = scraper.updater_get_all_ids(scraper)
    to_remove = [x for x in sheet_ids if x not in all_ids]
    spreadsheet = spreadsheet[~spreadsheet.id.isin(to_remove)]
    print(f"{len(to_remove)} products no longer on sale")
    to_add = [i for i in all_ids if  i not in sheet_ids]
    print(f"There are {len(to_add)} new products on sale")
    
    #new_info = [scraper.updater_add_info(scraper,all_ids[i], i) for i in all_ids if i not in sheet_ids]
    new_info = []
    
    done = 0
    for i in all_ids:
        if i not in sheet_ids:
            new_info.append(scraper.updater_add_info(scraper,all_ids[i], i))
            done += 1
            print(f"{done}/{len(to_add)}. Estimated time remaining: {scraper.time_estimate(scraper, done, len(to_add), start)}")
            #print(new_info)
            
    new_item_df = pd.DataFrame(new_info, columns=spreadsheet.columns)
    new_spreadsheet = pd.concat([new_item_df, spreadsheet], ignore_index = True)
    no_duplicates = new_spreadsheet.drop_duplicates(subset=['id'])
    no_duplicates.reset_index(drop=True)
    no_duplicates.to_excel("sale_items.xlsx")
    finish = time.time()-start
    print(finish)

    
def main():
    
    if input('New scrape ("0") or update ("1")? ') == "0":
        initial_scrape()
    else:
        update()
    
        


if __name__ == "__main__":
    
    main()
