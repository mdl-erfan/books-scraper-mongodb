import requests
from bs4 import BeautifulSoup
import datetime
import time
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["books_db"]
collection = db["books"]
# lets test Connection
client.admin.command("ping")
print("Connected to MongoDB Atlas!")

all_books = []
rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
for page_num in range(1,51):
    url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    print(f"found {len(books)} in page {page_num}")
    
    for book in books:
       #getting the title
        title = book.find("h3").find("a")["title"]
        #extract the price
        price= float(book.find("p", class_="price_color").text.strip()[1:])

        #Rating
        rating_word = book.find("p", class_="star-rating")["class"][1]
        # the rating is in words, we can convert it to numbers for feature MongoDB aggregation
        rating = rating_map[rating_word]
 
        book_url = "http://books.toscrape.com/catalogue/" + book.find("h3").find("a")["href"].replace("catalogue/", "")
    
        # fetch genre from book's individual page
        time.sleep(1)
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.content, "html.parser")
        breadcrumb = book_soup.find("ul", class_="breadcrumb")
        genre = breadcrumb.find_all("li")[2].text.strip()
        
        book_doc = {
            "title":      title,
            "price":      price,
            "rating":     rating,
            "genre":      genre,
            "url":        book_url,
            "scraped_at": datetime.datetime.now(datetime.UTC)
        }
        all_books.append(book_doc)
        collection.insert_one(book_doc)

print(all_books)
print(f"Total books scraped: {len(all_books)}")