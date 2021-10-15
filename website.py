import requests
from bs4 import BeautifulSoup
import csv
import math
import os
from category import category_scrape

url_books_to_scrape = "http://books.toscrape.com/"
index_page = requests.get(url_books_to_scrape)
soup = BeautifulSoup(index_page.content, 'html.parser')

book_categories = soup.find('ul', attrs={'class': 'nav-list'}).find_all('a')
book_categories.remove(book_categories[0])

for link_category in book_categories:
    href = link_category.get('href')
    print("url", url_books_to_scrape + href)
    category_scrape(url_books_to_scrape + href)






