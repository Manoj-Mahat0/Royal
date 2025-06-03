from fastapi import APIRouter, Depends, HTTPException
from utils.auth_dependencies import get_current_user_rolewise
from bson import ObjectId
from database import db

router = APIRouter()

@router.get("/my-cake-orders/details")
def get_all_my_cake_orders_details(current_user=Depends(get_current_user_rolewise)):
    user_id = str(current_user["id"])
    phone = current_user.get("phone_number", "")

    # Orders placed by the user (regular and designer)
    placed_orders = list(db.cake_orders.find({"user_id": user_id}))
    for order in placed_orders:
        order["_id"] = str(order["_id"])
        order["type"] = "placed"

    # Orders received by the user (delivered to their phone number)
    received_orders = list(db.cake_orders.find({
        "phone_number": phone,
        "status": "DELIVERED"
    }))
    for order in received_orders:
        order["_id"] = str(order["_id"])
        order["type"] = "received"

    # Remove duplicates if any (in case user placed and received the same order)
    seen_ids = set()
    all_orders = []
    for order in placed_orders + received_orders:
        if order["_id"] not in seen_ids:
            all_orders.append(order)
            seen_ids.add(order["_id"])

    return {"orders": all_orders}