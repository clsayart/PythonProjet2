import requests
from bs4 import BeautifulSoup
import csv
import math
import os

url_test = "http://books.toscrape.com/catalogue/the-past-never-ends_942/index.html"


def page_scrape(url):
    url_books_to_scrape = "http://books.toscrape.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    upc = soup.find(text="UPC").find_next().text
    title = soup.find('h1').string
    price_including_tax = soup.find(text="Price (incl. tax)").find_next().text
    price_excluding_tax = soup.find(text="Price (excl. tax)").find_next().text
    number_available = soup.find(text="Availability").find_next().text[10:12]
    product_description = soup.find(id="product_description").find_next_sibling().string
    category = soup.find(class_="breadcrumb").contents[5].text.replace("\n", "").replace("\r", "")
    review_rating = soup.find('p', attrs={'class': 'star-rating'})['class'][1]
    image = soup.find('div', attrs={'class': 'item'}).find('img')['src'][6:]
    image_url = url_books_to_scrape + image

    en_tete = ["url", "upc", "title", "price_including_tax", "price_excluding_tax", "category", "review_rating",
               "number_available",
               "product_description", "image_url"]
    line = [url, upc, title, price_including_tax, price_excluding_tax, category, review_rating, number_available,
            product_description, image_url]

    with open('data.csv', 'w') as file_csv:
        writer = csv.writer(file_csv, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow(line)


page_scrape(url_test)
