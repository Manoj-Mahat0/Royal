from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cake_shop_db"]

# Clear old data (optional)
if "cake_names" in db.list_collection_names():
    db.cake_names.delete_many({})

# 🎂 Cake flavor names and prices (edit prices as needed)
cake_price_data = [
    {"name": "Vanilla Cake", "prices": {1: 350, 2: 650, 3: 950}},
    {"name": "Black Forest Cake", "prices": {1: 400, 2: 750, 3: 1100}},
    {"name": "Black Forest Truffle Cake", "prices": {1: 420, 2: 800, 3: 1200}},
    {"name": "Pineapple Cake", "prices": {1: 360, 2: 670, 3: 980}},
    {"name": "Butterscotch Cake", "prices": {1: 380, 2: 720, 3: 1050}},
    {"name": "White Forest Cake", "prices": {1: 410, 2: 790, 3: 1150}},
    {"name": "Butterscotch Crunch Cake", "prices": {1: 430, 2: 820, 3: 1250}},
    {"name": "Chocolate Truffle Cake", "prices": {1: 450, 2: 850, 3: 1300}},
    {"name": "Choco Chips Cake", "prices": {1: 390, 2: 730, 3: 1080}},
    {"name": "Full Truffle Cake", "prices": {1: 470, 2: 900, 3: 1350}},
    {"name": "Belgium Chocolate Cake", "prices": {1: 500, 2: 950, 3: 1450}},
    {"name": "Extra Pineapple Cake", "prices": {1: 370, 2: 690, 3: 1000}},
    {"name": "Almond Truffle Cake", "prices": {1: 480, 2: 920, 3: 1380}},
    {"name": "Fresh Fruit Cake", "prices": {1: 520, 2: 980, 3: 1500}},
    {"name": "Blueberry Cake", "prices": {1: 530, 2: 1000, 3: 1550}},
    {"name": "Strawberry Cake", "prices": {1: 540, 2: 1020, 3: 1580}},
    {"name": "Red Velvet Cake", "prices": {1: 560, 2: 1050, 3: 1620}},
    {"name": "Yellow Panda Cake", "prices": {1: 370, 2: 690, 3: 1000}},
    {"name": "Teddy Bear Cake", "prices": {1: 600, 2: 1150, 3: 1750}},
    {"name": "American Forest Cake", "prices": {1: 580, 2: 1100, 3: 1680}},
    {"name": "Small Chocobar Cake", "prices": {1: 350, 2: 650, 3: 950}},
    {"name": "Big Chocobar Cake", "prices": {1: 700, 2: 1300, 3: 1900}},
    {"name": "Striped Chocolate Cake", "prices": {1: 480, 2: 920, 3: 1380}},
    {"name": "Lollipop Cake", "prices": {1: 390, 2: 730, 3: 1080}},
    {"name": "Cheesecake Jar", "prices": {1: 200, 2: 380, 3: 550}},
    {"name": "Heart-Shaped Chocolate Cake", "prices": {1: 600, 2: 1150, 3: 1750}},
]

# Prepare cake documents for each weight
cake_docs = []
for cake in cake_price_data:
    for weight, price in cake["prices"].items():
        cake_docs.append({
            "name": cake["name"],
            "weight_lb": weight,
            "price": price,
            "description": f"A delicious {cake['name'].lower()} available in {weight} lb."
        })

# Insert into MongoDB
result = db.cake_names.insert_many(cake_docs)
print(f"✅ Inserted {len(result.inserted_ids)} cake names with prices successfully.")