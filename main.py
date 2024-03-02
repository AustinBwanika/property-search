
FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSee1usI0tR7t1MSwdelvmhDAq4Uvrb9s5imMKhQ_x2YvYqMlg/viewform?usp=sf_link'
import threading
import time
from selenium import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests

from bs4 import BeautifulSoup as bs, BeautifulSoup

website_url = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E580&maxBedrooms=4&minBedrooms=2&propertyTypes=flat%2Cprivate-halls&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='

r = requests.get('https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E580&maxBedrooms=4&minBedrooms=2&propertyTypes=flat%2Cprivate-halls&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=')
# convert to beautiful soup
soup = bs(r.content, features="html.parser")

# scrapping the links:-
# For all the 'href' links

# web_links = soup.select('a')

CHROME_DRIVER_PATH = "/Users/austinkasekende/Desktop/CodeWork/Development/chromedriver"

services = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=services)

driver.get(url='https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E580&maxBedrooms=4&minBedrooms=2&propertyTypes=flat%2Cprivate-halls&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=')
prices = driver.find_elements(By.CLASS_NAME, 'propertyCard-priceValue')
description = driver.find_elements(By.CLASS_NAME,'propertyCard-description')


final_links_list = []

try:
    # Send an HTTP GET request to the specified URL
    response = requests.get(website_url)
    response.raise_for_status()  # Raise an exception if there's an error with the request

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response.text)
    # Find all anchor tags (a) and extract the href attribute to get the links
    links = [f"https://www.rightmove.co.uk{a['href']}" for a in soup.find_all('a', class_='propertyCard-link')]
    # https://www.rightmove.co.uk
    # Append the links to the final_links_list
    for i in links:
        if i not in final_links_list:
            final_links_list.append(i)


except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")


final_price_list = [i.text for i in prices]
final_description_list = [i.text for i in description]


# print(len(final_price_list))
# print(len(final_description_list))
# print(len(final_links_list))
# print(final_links_list)


# Google form fill in
for i in range(0,len(final_price_list)):
    driver.get(url=FORM)

    description = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/textarea')
    description.click()
    time.sleep(2)
    description.send_keys(f"{final_description_list[i]}")

    price_per_month = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_per_month.click()
    time.sleep(2)
    price_per_month.send_keys(f"{final_price_list[i]}")

    property_link = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link.click()
    time.sleep(2)
    property_link.send_keys(f"{final_links_list[i]}")

    submit_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(5)




time.sleep(10000)


