from pymongo import MongoClient
import random

# Connect to MongoDB
client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cake_shop_db"]

# Optional: clear existing flavors
db.flavors.delete_many({})
print("🧹 Cleared previous documents from 'flavors' collection")

# Define 5 flavors
flavor_docs = [
    {
        "name": "Vanilla Cake",
        "quantities": {
            "1lbs": {"price": random.randint(350, 500), "quantity": 1},
            "2lbs": {"price": random.randint(650, 900), "quantity": 1},
            "3lbs": {"price": random.randint(950, 1300), "quantity": 1}
        }
    },
    {
        "name": "Chocolate Truffle Cake",
        "quantities": {
            "1lbs": {"price": random.randint(400, 600), "quantity": 1},
            "2lbs": {"price": random.randint(700, 1000), "quantity": 1},
            "3lbs": {"price": random.randint(1000, 1400), "quantity": 1}
        }
    },
    {
        "name": "Red Velvet Cake",
        "quantities": {
            "1lbs": {"price": random.randint(450, 650), "quantity": 1},
            "2lbs": {"price": random.randint(750, 1050), "quantity": 1},
            "3lbs": {"price": random.randint(1050, 1450), "quantity": 1}
        }
    },
    {
        "name": "Black Forest Cake",
        "quantities": {
            "1lbs": {"price": random.randint(380, 520), "quantity": 1},
            "2lbs": {"price": random.randint(700, 950), "quantity": 1},
            "3lbs": {"price": random.randint(950, 1300), "quantity": 1}
        }
    },
    {
        "name": "Butterscotch Cake",
        "quantities": {
            "1lbs": {"price": random.randint(370, 500), "quantity": 1},
            "2lbs": {"price": random.randint(680, 900), "quantity": 1},
            "3lbs": {"price": random.randint(950, 1250), "quantity": 1}
        }
    }
]

# Insert data
result = db.flavors.insert_many(flavor_docs)
print(f"✅ Inserted {len(result.inserted_ids)} flavors into 'cake_shop_db.flavors'")
