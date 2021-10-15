import requests
from bs4 import BeautifulSoup
import csv
import math
import os

url_test = "http://books.toscrape.com/catalogue/category/books/self-help_41/index.html"


def category_scrape(url):
    links = []
    url_books_to_scrape_catalogue = "http://books.toscrape.com/catalogue"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    number_of_page = soup.find('form', attrs={'class': 'form-horizontal'}).contents[3].text
    category_name = soup.find('div', attrs={'class': 'page-header'}).h1.text
    int_number_of_page = int(number_of_page)

    if math.ceil(int_number_of_page / 20) == 1:
        links.append(url)
    else:
        for i in range(1, math.ceil(int_number_of_page / 20) + 1):
            url_page_test = url[:-10] + "page-" + str(i) + '.html'
            links.append(url_page_test)

    url_books = []
    for link in links:
        print("link", link)
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        href = soup.find('ol', attrs={'class': 'row'}).find_all('a')
        for lien in href:
            book_url = url_books_to_scrape_catalogue + lien.get('href')[8:]
            if book_url not in url_books:
                url_books.append(book_url)

    def page_scrape(url):
        url_books_to_scrape = "http://books.toscrape.com/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        upc = soup.find(text="UPC").find_next().text
        title = soup.find('h1').string
        price_including_tax = soup.find(text="Price (incl. tax)").find_next().text
        price_excluding_tax = soup.find(text="Price (excl. tax)").find_next().text
        number_available = soup.find(text="Availability").find_next().text[10:12]
        try:
            product_description = soup.find(id="product_description").find_next_sibling().string
        except:
            product_description = "unknown"
        category = soup.find(class_="breadcrumb").contents[5].text.replace("\n", "").replace("\r", "")
        review_rating = soup.find('p', attrs={'class': 'star-rating'})['class'][1]
        image = soup.find('div', attrs={'class': 'item'}).find('img')['src'][6:]
        image_name = soup.find('div', attrs={'class': 'item'}).find('img')['alt']
        image_url = url_books_to_scrape + image
        image_store(image_url, image_name)
        # lui faire un request get image url (comme dans fonction image store)

        en_tete = ["url", "upc", "title", "price_including_tax", "price_excluding_tax", "category", "review_rating",
                   "number_available",
                   "product_description", "image_url"]
        line = [url, upc, title, price_including_tax, price_excluding_tax, category, review_rating, number_available,
                product_description, image_url]

        with open(category_name + '.csv', 'a') as file_csv:
            writer = csv.writer(file_csv, delimiter=',')
            if url == url_books[0]:
                writer.writerow(en_tete)
                writer.writerow(line)
            else:
                writer.writerow(line)

    for url_book in url_books:
        page_scrape(url_book)


def image_store(url, name):
    try:
        os.mkdir(os.path.join(os.getcwd(), "images"))
        os.chdir(os.path.join(os.getcwd(), "images"))
    except:
        os.chdir(os.path.join(os.getcwd(), "images"))
    with open(name.replace(' ', '-').replace('/', '-') + '.jpg', 'wb') as f:
        im = requests.get(url)
        f.write(im.content)
        print('Writing: ', name)
    os.chdir('..')


category_scrape(url_test)
