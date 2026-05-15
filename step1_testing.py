import requests
from bs4 import BeautifulSoup
import datetime
import time

url = "http://books.toscrape.com"

# lets check the website and get the status code of the response
response = requests.get(url)
print(response.status_code)

soup = BeautifulSoup(response.content, "html.parser")
books = soup.find_all("article", class_="product_pod")
print(f"found {len(books)} books on this page")

# have a look at the first book
first_book = books[0]
print(first_book)

# extract the title and price of the first book
#extract the title
title = first_book.find("h3").find("a")["title"]

#extract the price
price= float(first_book.find("p", class_="price_color").text.strip()[1:])

#Rating
rating_word = first_book.find("p", class_="star-rating")["class"][1]

print(f"Title  : {title}")
print(f"Price  : {price}")
print(f"Rating : {rating_word}")

# the rating is in words, we can convert it to numbers for feature MongoDB aggregation

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}
rating = rating_map[rating_word]
print(f"Rating as Number :{rating} ")

#url of the book
book_url = "http://books.toscrape.com/" + first_book.find("h3").find("a")["href"]
print(f"Book URL : {book_url}")

# getting Genre of the book(it is in the navigation bar in book url page )
book_response = requests.get(book_url)
book_soup = BeautifulSoup(book_response.content, "html.parser")

breadcrumb = book_soup.find("ul", class_="breadcrumb")
print(breadcrumb)
# poetry is at index 2 in the breadcrumb list
genre = breadcrumb.find_all("li")[2].text.strip()
print(f"Genre : {genre}")

#putting book into a dictionary
book = {
    "title" : title,
    "price" : price,
    "rating" : rating,
    "genre" : genre,
    "url" : book_url,
    "scraped_at" : datetime.datetime.now(datetime.UTC)
}
print(book)