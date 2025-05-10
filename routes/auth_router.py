from fastapi import APIRouter, HTTPException
from models.user_model import UserLogin
from database import db
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
