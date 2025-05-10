from pymongo import MongoClient

client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cake_shop_db"]

cake_data = [
    {
        "category": "Based on Texture",
        "cakes": [
            {"name": "Sponge Cake", "description": "Light and airy, made without butter (e.g., Chiffon, Angel Food)"},
            {"name": "Butter Cake", "description": "Rich and moist, made with creamed butter (e.g., Vanilla, Chocolate)"},
            {"name": "Pound Cake", "description": "Dense, made with equal parts butter, sugar, flour, and eggs"},
            {"name": "Foam Cake", "description": "Uses whipped eggs for volume (e.g., Genoise, Biscuit Cake)"}
        ]
    },
    {
        "category": "Popular Flavors",
        "cakes": [
            {"name": "Chocolate Cake"},
            {"name": "Vanilla Cake"},
            {"name": "Red Velvet Cake"},
            {"name": "Black Forest Cake"},
            {"name": "Coffee Cake"},
            {"name": "Fruit Cake"}
        ]
    },
    {
        "category": "Specialty Cakes",
        "cakes": [
            {"name": "Cheesecake", "description": "Cream cheese-based, no flour"},
            {"name": "Ice Cream Cake", "description": "Layers of cake and ice cream"},
            {"name": "Molten Lava Cake", "description": "With gooey chocolate center"},
            {"name": "Carrot Cake", "description": "With grated carrots and nuts"}
        ]
    },
    {
        "category": "Occasion-Based",
        "cakes": [
            {"name": "Birthday Cake"},
            {"name": "Wedding Cake"},
            {"name": "Anniversary Cake"},
            {"name": "Theme Cakes", "description": "E.g., cartoon, floral, customized"}
        ]
    }
]

# Insert into collection
db.cake_categories.insert_many(cake_data)
print("✅ Cake categories inserted successfully.")
