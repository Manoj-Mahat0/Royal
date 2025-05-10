from pymongo import MongoClient

client = MongoClient("mongodb+srv://manojmahato08779:ngnyH6RFix5CdO4D@cluster0.9cqyq0s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cake_shop_db"]

db.users.insert_one({
    "full_name": "Manoj Main Store",
    "phone_number": "9876543210",
    "dob": "1990-01-01",
    "role": "MAIN_STORE"
})

print("✅ MAIN_STORE user inserted successfully.")
