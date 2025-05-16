# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = client["cake_shop_db"]

# # Your updated list of cake names
# cake_names = [
#     "Vanilla Cake",
#     "Black Forest Cake",
#     "Black Forest Truffle Cake",
#     "Pineapple Cake",
#     "Butterscotch Cake",
#     "White Forest Cake",
#     "Butterscotch Crunch Cake",
#     "Chocolate Truffle Cake",
#     "Choco Chips Cake",
#     "Full Truffle Cake",
#     "Belgium Chocolate Cake",
#     "Extra Pineapple Cake",
#     "Almond Truffle Cake",
#     "Fresh Fruit Cake",
#     "Blueberry Cake",
#     "Strawberry Cake",
#     "Red Velvet Cake",
#     "Yellow Panda Cake",
#     "Teddy Bear Cake",
#     "American Forest Cake",
#     "Small Chocobar Cake",
#     "Big Chocobar Cake",
#     "Striped Chocolate Cake",
#     "Lollipop Cake",
#     "Cheesecake Jar",
#     "Heart-Shaped Chocolate Cake"
# ]


# # Convert to document format
# cake_docs = [{"name": name} for name in cake_names]

# # Clear existing entries (optional)
# db.cake_names.delete_many({})

# # Insert new cake names
# result = db.cake_names.insert_many(cake_docs)

# print(f"✅ Inserted {len(result.inserted_ids)} cake names successfully.")


from pymongo import MongoClient
import random

# Connect to MongoDB
client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Use a new database
db = client["cake_shop_db"]

# Check if collection exists, then clear it
if "cake_names" in db.list_collection_names():
    db.cake_names.delete_many({})

# Cake names
cake_names = [
    "Vanilla Cake", "Black Forest Cake", "Black Forest Truffle Cake", "Pineapple Cake",
    "Butterscotch Cake", "White Forest Cake", "Butterscotch Crunch Cake", "Chocolate Truffle Cake",
    "Choco Chips Cake", "Full Truffle Cake", "Belgium Chocolate Cake", "Extra Pineapple Cake",
    "Almond Truffle Cake", "Fresh Fruit Cake", "Blueberry Cake", "Strawberry Cake",
    "Red Velvet Cake", "Yellow Panda Cake", "Teddy Bear Cake", "American Forest Cake",
    "Small Chocobar Cake", "Big Chocobar Cake", "Striped Chocolate Cake", "Lollipop Cake",
    "Cheesecake Jar", "Heart-Shaped Chocolate Cake"
]

# Prepare documents
cake_docs = []
for name in cake_names:
    for weight in [1, 2, 3]:
        price = random.randint(300, 700) * weight
        description = f"A delicious {name.lower()} available in {weight} lb."
        cake_docs.append({
            "name": name,
            "weight_lb": weight,
            "price": price,
            "description": description
        })

# Insert data
result = db.cake_names.insert_many(cake_docs)
print(f"✅ Inserted {len(result.inserted_ids)} cake variants successfully into 'cake_shop_inventory' database.")
