from selenium import webdriver
import time
import random
import os

search_term = f'아이스크림'
PATH_DIR = f'IceCream'

if not os.path.exists(PATH_DIR):
    os.mkdir(f'./Data/{PATH_DIR}')
    print("Directory " , PATH_DIR ,  " Created ")
else:
    print("Directory " , PATH_DIR ,  " already exists")

url = f'https://www.google.com/search?q={search_term}&tbm=isch'

browser = webdriver.Chrome(f'./chromedriver')
browser.get(url)

for i in range(200):
    browser.execute_script(f'window.scrollBy(0,10000)')


for idx, el in enumerate(browser.find_elements_by_class_name(f'rg_i')):
    el.screenshot(f'./Data/{PATH_DIR}/{idx}.jpg')
    time.sleep(random.randint(1, 3))