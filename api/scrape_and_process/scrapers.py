import requests
from bs4 import BeautifulSoup
import threading
import os

#For when the website blocks requests (and so I don't have to rewrite)
from selenium import webdriver
from selenium.webdriver.common.by import By


#Same for all since all websites have blockers that make it annoying to extract images
def get_img_from_google(query):
    link = f'https://www.google.com/search?q={query.lower().replace(" ", "+")}&tbm=isch'
    req = requests.get(link)
    parser = BeautifulSoup(req.content, 'html.parser')
    img_links = [i['src'] for i in parser.findAll("img") if "gif" not in i['src']]
    return img_links[0]
    

#Getting data for nike/jordan drops via snkrs
def get_nike_drops():
    snkrs_link = "https://nike.com/launch?s=upcoming"

    req = requests.get(snkrs_link, headers = {'User-agent': 'Mozilla/5.0'})
    parser = BeautifulSoup(req.content, 'html.parser')
    shoe_links = [e['href'] for e in parser.find_all('a', {'class' : 'card-link d-sm-b'})]

    snkrs_data = []
    names = []

    def process_link(link):
        full_link = "https://nike.com" + link.replace('/it', '')
        req = requests.get(full_link)
        parser = BeautifulSoup(req.content, 'html.parser')
        try:
            shoe = parser.find('h1', {'class' : 'headline-5'}).decode_contents()
            if shoe in names:
                raise Exception("Duplicate shoe")
                
            names.append(shoe)
            colorway = parser.find('h2', {'class' : 'headline-1'}).decode_contents()
            price = parser.find('div', {'class' : 'headline-5'}).decode_contents()
            release_date = parser.find('div', {'class' : 'available-date-component'}).decode_contents()
            

            price = float(price.replace("$", ""))
            brand = 'Nike'
            if 'Jordan' in shoe:
                brand = 'Jordan'

            snkrs_data.append({
                'name' : shoe + " " + colorway, 'price' : price, 'release_date' : release_date, 'link' : full_link,
                'brand' : brand, 'img_link' : get_img_from_google(shoe + " " + colorway)
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
#UPDATE: Website blocked by bots
def get_new_balance_drops():
    nb_data = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-dev-shm-usage')  
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
                'name' : "New Balance " + name, 'price' : price, 'release_date' : release_date, 'link' : link, 
                'brand' : 'new balance',  'img_link' : get_img_from_google("New Balance " + name)
            }) #Image link is placeholder due to site being down
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
    root = "https://www.adidas.com"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-dev-shm-usage')  
    chrome_options.add_argument('--headless=new')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(adidas_link)
    src = driver.page_source
    driver.quit()
    
    #Parsing after because the page dynamically changed content while parsing, throwing errors
    parser = BeautifulSoup(src, "html.parser")
    product_divs = parser.find_all("div", {"class" : "plc-product-details-info"})
    product_links = [root + a['href'] for a in parser.find_all("a") if a.has_attr("class") and "_plc-product-link" in ' '.join(a['class'])]
    
    adidas_data = []
    names = []
    
    def handle(link, div):
        try:
            date = div.find("strong").decode_contents(); 
            price = div.find("div", {"class" : "gl-price-item"}).decode_contents(); 
            name = [d.decode_contents() for d in div.find_all("div") if '_plc-product-name' in ' '.join(d['class'])][0]
            if name in names:
                raise Exception("Duplicate Shoe")

            names.append(name)
            price = float(price.replace("$", ''))

            adidas_data.append({
                'release_date' : date, 'name' : "Adidas " + name, 'price' : price, 'link' : link,
                'brand' : 'adidas', 'img_link' : get_img_from_google("Adidas "  + name)
            })
        except Exception as e:
            pass
    
    threads = []
    for link, div in zip(product_links, product_divs):
        t = threading.Thread(target = handle, args = (link, div))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return adidas_data
