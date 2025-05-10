from fastapi import APIRouter, Depends, HTTPException
from models.store_model import StoreCreate
from models.user_model import AddUser
from database import db
from utils.auth_dependencies import get_current_user
from bson import ObjectId

router = APIRouter()

def serialize_store(store: dict):
    store["_id"] = str(store.get("_id", ""))
    store["owner_id"] = str(store.get("owner_id", ""))
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
    new_user["loyalty_points"] = 50  # ✅ Add 50 loyalty points

    db.users.insert_one(new_user)  # ✅ This updates MongoDB

    return {
        "message": f"{new_user['role']} user created successfully with 50 loyalty points.",
        "user": {
            "full_name": new_user["full_name"],
            "phone_number": new_user["phone_number"],
            "role": new_user["role"],
            "loyalty_points": new_user["loyalty_points"]
        }
    }
@router.get("/all")
def get_all_store_names():
    stores = db.stores.find({}, {"name": 1})  # Only fetch name field
    return [{"_id": str(s["_id"]), "name": s["name"]} for s in stores]