from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from models.user_model import UserLogin
from database import db
from utils.auth_dependencies import get_current_user_rolewise
from utils.jwt_helper import create_token

router = APIRouter()

@router.post("/login")
def login(payload: UserLogin):
    user = db.users.find_one({
        "phone_number": payload.phone_number,
        "dob": payload.dob
    })
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token({"id": str(user["_id"]), "role": user["role"]})
    return {
        "access_token": token,
        "user": {
            "name": user["full_name"],
            "role": user["role"]
        }
    }



@router.get("/me/store-name")
def get_store_name(user=Depends(get_current_user_rolewise)):
    user_id = user["id"]
    user_role = user["role"]

    print(f"[DEBUG] Current user ID: {user_id}, Role: {user_role}")

    if user_role not in ["SUB_STORE", "FACTORY", "MAIN_STORE"]:
        raise HTTPException(status_code=403, detail="User is not a store")

    query = {"$or": []}

    # Owner-based match (MAIN_STORE, FACTORY)
    query["$or"].append({"owner_id": user_id})
    if ObjectId.is_valid(user_id):
        query["$or"].append({"owner_id": ObjectId(user_id)})
        query["$or"].append({"_id": ObjectId(user_id)})

    # Linked user ID match (for SUB_STORE logins that are separate from store doc)
    query["$or"].append({"linked_user_id": user_id})

    print(f"[DEBUG] Final query to find store: {query}")

    store = db.stores.find_one(query)

    if not store:
        print("[ERROR] Store not found for this user.")
        raise HTTPException(status_code=404, detail="Store not found")

    print(f"[SUCCESS] Store found: {store['name']} (ID: {store['_id']})")

    return {
        "store_name": store["name"],
        "store_id": str(store["_id"])
    }


