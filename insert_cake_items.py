from pymongo import MongoClient

client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cake_shop_db"]

# 🎂 Cake Bases
cake_bases = [
    {"name": "Sponge Cake"},
    {"name": "Butter Cake"},
    {"name": "Pound Cake"},
    {"name": "Foam Cake"}
]

# 🍫 Flavors
flavors = [
    {"name": "Chocolate Cake"},
    {"name": "Vanilla Cake"},
    {"name": "Red Velvet Cake"},
    {"name": "Black Forest Cake"},
    {"name": "Coffee Cake"},
    {"name": "Fruit Cake"}
]

# 🥜 Ingredients
ingredients = [
    {"name": "Nuts"},
    {"name": "Cherries"},
    {"name": "Fresh Cream"},
    {"name": "Fruit Slices"},
    {"name": "Sprinkles"},
    {"name": "Chocolate Chips"}
]

# 🎨 Designs
designs = [
    {"name": "Birthday Cake"},
    {"name": "Wedding Cake"},
    {"name": "Anniversary Cake"},
    {"name": "Cartoon Theme"},
    {"name": "Floral Design"}
]

# Insert into DB
db.cake_bases.insert_many(cake_bases)
db.flavors.insert_many(flavors)
db.ingredients.insert_many(ingredients)
db.designs.insert_many(designs)

print("✅ Cake options inserted successfully.")
