import requests
from bs4 import BeautifulSoup
import threading
import os

#For when the website blocks requests (and so I don't have to rewrite)
from selenium import webdriver
from selenium.webdriver.common.by import By


#Getting data for nike/jordan drops via snkrs
def get_nike_drops():
    snkrs_link = "https://nike.com/launch?s=upcoming"

    req = requests.get(snkrs_link, headers = {'User-agent': 'Mozilla/5.0'})
    parser = BeautifulSoup(req.content, 'html.parser')
    shoe_links = [e['href'] for e in parser.find_all('a', {'class' : 'card-link d-sm-b'})]

    snkrs_data = []


    def process_link(link):
        full_link = "https://nike.com" + link.replace('/it', '')
        req = requests.get(full_link)
        parser = BeautifulSoup(req.content, 'html.parser')
        try:
            shoe = parser.find('h1', {'class' : 'headline-5'}).decode_contents()
            colorway = parser.find('h2', {'class' : 'headline-1'}).decode_contents()
            price = parser.find('div', {'class' : 'headline-5'}).decode_contents()
            release_date = parser.find('div', {'class' : 'available-date-component'}).decode_contents()

            price = float(price.replace("$", ""))
            release_datedate = release_date.split(' ')[1]

            brand = 'Nike'
            if 'Jordan' in shoe:
                brand = 'Jordan'

            snkrs_data.append({
                'name' : shoe + " " + colorway, 'price' : price, 'release_date' : release_date, 'link' : full_link,
                'brand' : brand
            })
        except:
            pass #Assume the product found isn't a sneaker

    threads = []

    for link in shoe_links:
        if "/launch/t" in link:
            thread = threading.Thread(target = process_link, args = (link, ))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()


    return snkrs_data




#Getting new balance drops
def get_new_balance_drops():
    nb_data = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--log-levels=3')
    driver = webdriver.Chrome(options = chrome_options)

    nb_link = 'https://www.newbalance.com/nb-launches/'
    driver.get(nb_link)
    shoes = driver.find_elements(By.CSS_SELECTOR, 'a.product')
    links = [shoe.get_property('href') for shoe in shoes]

    driver.quit()

    def process_link(link):
        try:
            driver = webdriver.Chrome(options = chrome_options)
            driver.get(link)
            name = driver.find_element(By.CSS_SELECTOR, 'h1.product-name.hidden-sm-down').get_property('innerHTML')
            price = driver.find_element(By.CSS_SELECTOR, 'span.sales.font-body-large').get_property('innerHTML')
            release_date = driver.find_element(By.CSS_SELECTOR, 'span.date').get_property('innerHTML')
            nb_data.append({
                'name' : "New Balance " + name, 'price' : price, 'release_date' : release_date, 'link' : link, 'brand' : 'new balance'
            })
            driver.quit()
        except: #Assume the link isn't for a shoe
            pass 

    threads = []

    for link in links:
        thread = threading.Thread(target = process_link, args = (link, ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    driver.quit()
    return nb_data



#Getting adidas drops
def get_adidas_drops():
    adidas_link = "https://www.adidas.com/us/release-dates"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless=new')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options = chrome_options)

    driver.get(adidas_link)
    dates = [i.find_element(By.CSS_SELECTOR, 'strong').get_property('innerHTML') for i in driver.find_elements(By.CSS_SELECTOR, "div._plc-product-date_1xwgu_180")]
    shoe_names = [i.get_property('innerHTML') for i in driver.find_elements(By.CSS_SELECTOR, 'div._plc-product-name_1xwgu_161')]
    prices = [i.get_property('innerHTML') for i in driver.find_elements(By.CSS_SELECTOR, 'div.gl-price-item')]
    links = [i.get_property('href') for i in driver.find_elements(By.CSS_SELECTOR, 'a._plc-product-link_1xwgu_57')]

    driver.quit()

    adidas_data = []
    for date, shoe_name, price, link in zip(dates, shoe_names, prices, links):
        try:
            price = float(price.replace("$", ""))
            date = date.split(" ")[1] + " " + date.split(" ")[2]

            adidas_data.append({
                'release_date' : date, 'name' : "Adidas " + shoe_name, 'price' : price, 'link' : link, 'brand' : 'adidas'
            })
        
        except: #Same assumption that product isn't a shoe
            pass

    return adidas_data



