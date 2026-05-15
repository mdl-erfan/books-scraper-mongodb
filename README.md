# Books Scraper with MongoDB

A web scraping project that collects book data from [books.toscrape.com](http://books.toscrape.com) and stores it in MongoDB. The goal is to answer two business questions:

- Which book genres have the **highest average rating**?
- Which book genres are the **most affordable** on average?

---

## What This Project Does

1. Scrapes all 1000 books from books.toscrape.com (50 pages)
2. For each book, it collects: title, price, rating, genre, and URL
3. Saves everything into a MongoDB database
4. Runs analysis queries to rank genres by rating and price

---

## Project Files

| File | What it does |
|---|---|
| `scrape.py` | Scrapes the website and saves data to MongoDB |
| `analysis.py` | Runs queries on MongoDB and prints the results |
| `requirements.txt` | List of Python packages needed |
| `.env` | Your MongoDB connection string (not shared) |

---

## Requirements

- Python 3.8 or higher
- A MongoDB Atlas account (free tier is fine) — [Sign up here](https://www.mongodb.com/cloud/atlas)

---

## Setup Steps

### Step 1 — Download the project

```bash
git clone https://github.com/mdl-erfan/books-scraper-mongodb.git
cd books-scraper-mongodb
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- On Mac/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### Step 3 — Install the required packages

```bash
pip install -r requirements.txt
```

### Step 4 — Set up your MongoDB connection

Create a file called `.env` in the project folder and add this line:

```
MONGO_URI=your_mongodb_connection_string_here
```

Replace `your_mongodb_connection_string_here` with your actual connection string from MongoDB Atlas.

> To get your connection string: go to MongoDB Atlas → your cluster → Connect → Drivers → copy the string.

### Step 5 — Run the scraper

```bash
python scrape.py
```

This will scrape all 1000 books and save them to MongoDB. It takes a few minutes because it visits each book's page to get the genre.

### Step 6 — Run the analysis

```bash
python analysis.py
```

This will print two results:

- Top 10 genres by average rating
- Top 10 most affordable genres by average price

---

## Example Output

```
-------> Top 10 Genre By Average rating <--------
 Mystery : 4.5
 Classics : 4.3
 ...

-----> Top 10 Affordable Genres <-----
Poetry : 23.4
Crime : 25.1
...
```

---

## Notes

- The scraper uses a 1-second delay between requests to be polite to the website
- Data is stored in a database called `books_db`, in a collection called `books`
- Make sure your `.env` file is never shared or pushed to GitHub
