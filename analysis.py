from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
collection = client["books_db"]["books"]
if client.admin.command("ping"):
    print(f"Connected to MongoDB, and Total books {collection.count_documents({})}")

pipeline1= [
    {"$group":
        {
            "_id":"$genre",
            "avg_rating":{"$avg":"$rating"}
        }

    },
    {"$sort":
        {
            "avg_rating": -1
        }

    },
    {"$limit":
        10

    }
]


pipeline2 = [
    {"$group": 
            {
                "_id":"$genre",
                "avg_price":{"$avg":"$price"}
            }
    },
    {"$sort":
        {
            "avg_price": 1
        }

    },
    {"$limit":
        
            10
        

    }
]
print("\n-------> Top 10 Genre By Average rating <--------")
for result in collection.aggregate(pipeline1):
    print(f" {result['_id']} : {result['avg_rating']} ")

print("\n -----> Top 10 Affordable Genres <-----")
for result in collection.aggregate(pipeline2):
    print(f"{result['_id']} : {result['avg_price']}")