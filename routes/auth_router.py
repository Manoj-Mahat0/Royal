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
    if user["role"] not in ["SUB_STORE", "FACTORY", "MAIN_STORE"]:
        raise HTTPException(status_code=403, detail="User is not a store")

    store = db.stores.find_one({"owner_id": ObjectId(user["id"])})
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    return {
        "store_name": store["name"],
        "store_id": str(store["_id"])  # Ensure ObjectId is converted to string
    }
