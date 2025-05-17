from pymongo import MongoClient
import random

# Connect to MongoDB
client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cake_shop_db"]

# Clear old data (optional)
if "cake_variants" in db.list_collection_names():
    db.cake_variants.delete_many({})

# 🎂 Cake flavor names
cake_names = [
    "Vanilla Cake", "Black Forest Cake", "Black Forest Truffle Cake", "Pineapple Cake",
    "Butterscotch Cake", "White Forest Cake", "Butterscotch Crunch Cake", "Chocolate Truffle Cake",
    "Choco Chips Cake", "Full Truffle Cake", "Belgium Chocolate Cake", "Extra Pineapple Cake",
    "Almond Truffle Cake", "Fresh Fruit Cake", "Blueberry Cake", "Strawberry Cake",
    "Red Velvet Cake", "Yellow Panda Cake", "Teddy Bear Cake", "American Forest Cake",
    "Small Chocobar Cake", "Big Chocobar Cake", "Striped Chocolate Cake", "Lollipop Cake",
    "Cheesecake Jar", "Heart-Shaped Chocolate Cake"
]

# 📦 Prepare cake documents with random prices
cake_docs = []
for name in cake_names:
    for weight in [1, 2, 3]:  # lbs
        price = random.randint(300, 700) * weight
        description = f"A delicious {name.lower()} available in {weight} lb."
        cake_docs.append({
            "name": name,
            "weight_lb": weight,
            "price": price,
            "description": description
        })

# Insert into MongoDB
result = db.cake_variants.insert_many(cake_docs)
print(f"✅ Inserted {len(result.inserted_ids)} cake variants successfully.")
