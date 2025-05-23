from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from utils.email_helper import send_birthday_email, send_email
from models.store_model import StoreCreate
from models.user_model import AddUser
from database import db
from utils.auth_dependencies import get_current_user
from bson import ObjectId

router = APIRouter()


def serialize_store(store: dict):
    store["_id"] = str(store.get("_id", ""))
    store["owner_id"] = str(store.get("owner_id", ""))
    store["latitude"] = store.get("latitude")
    store["longitude"] = store.get("longitude")
    return store


@router.post("/create")
def create_store(store: StoreCreate, user=Depends(get_current_user)):
    if user["role"] != "MAIN_STORE":
        raise HTTPException(status_code=403, detail="Only MAIN_STORE can create new stores.")

    # Step 1: Insert into stores collection
    new_store = store.dict()
    new_store["owner_id"] = ObjectId(user["id"])
    db.stores.insert_one(new_store)

    # Step 2: Create login user for the store
    existing_user = db.users.find_one({"phone_number": store.phone_number})
    if existing_user:
        raise HTTPException(status_code=409, detail="Phone number already registered.")

    db.users.insert_one({
        "full_name": store.name,
        "phone_number": store.phone_number,
        "dob": store.dob,
        "role": store.type,
        "parent_store_id": ObjectId(user["id"])
    })

    return {
        "message": f"{store.type} created successfully with login access",
        "store": serialize_store(new_store)
    }


@router.post("/add-user")
def add_user(payload: AddUser):
    if db.users.find_one({"phone_number": payload.phone_number}):
        raise HTTPException(status_code=409, detail="User already exists with this phone number.")

    new_user = payload.dict()
    new_user["loyalty_points"] = 0

    db.users.insert_one(new_user)

    # ✅ Send welcome email
    subject = "🎉 Welcome to Cake Shop!"
    message = f"""
Hello {new_user['full_name']},<br><br>
Welcome to <strong>Cake Shop</strong>! You've earned <strong>0 loyalty points</strong> just for joining us. 🎂<br><br>
Here are your details:<br>
<strong>Phone Number:</strong> {new_user['phone_number']}<br>
<strong>Password:</strong> {new_user['dob']}<br><br>
We’re thrilled to have you with us! 🥳
"""

    recipient_email = new_user.get("email") or new_user["phone_number"] + "@example.com"
    send_email(to_email=recipient_email, to_name=new_user["full_name"], subject=subject, message=message)

    return {
        "message": f"{new_user['role']} user created successfully with 50 loyalty points.",
        "user": {
            "full_name": new_user["full_name"],
            "phone_number": new_user["phone_number"],
            "email": new_user["email"],
            "role": new_user["role"],
            "loyalty_points": new_user["loyalty_points"]
        }
    }


@router.get("/all")
def get_all_store_names():
    stores = db.stores.find({}, {"name": 1, "latitude": 1, "longitude": 1})
    return [
        {
            "_id": str(s["_id"]),
            "name": s["name"],
            "latitude": s.get("latitude"),
            "longitude": s.get("longitude")
        } for s in stores
    ]


@router.post("/send-auto-birthday-wishes")
def send_birthday_emails_from_db():
    today = datetime.now()
    today_str = today.strftime("%m-%d")  # e.g., '05-10'

    success_list = []
    fail_list = []

    users = db.users.find()
    for user in users:
        dob = user.get("dob", "")  # Expected format: 'YYYY-MM-DD'
        email = user.get("email") or user.get("phone_number") + "@example.com"  # fallback
        name = user.get("full_name", "Customer")

        if dob:
            try:
                dob_date = datetime.strptime(dob, "%Y-%m-%d")
                if dob_date.strftime("%m-%d") == today_str:
                    message = f"Happy Birthday, {name}! 🎉 Enjoy your day with a delicious cake from us!"
                    sent = send_birthday_email(to_email=email, to_name=name, custom_message=message)
                    (success_list if sent else fail_list).append(email)
            except Exception as e:
                fail_list.append(email)

    return {
        "sent": success_list,
        "failed": fail_list,
        "summary": f"{len(success_list)} emails sent, {len(fail_list)} failed"
    }
