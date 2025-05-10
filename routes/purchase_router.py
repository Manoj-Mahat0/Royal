from fastapi import APIRouter, HTTPException
from models.purchase_model import PurchaseRequest
from database import db

router = APIRouter()

@router.post("/")
def handle_purchase(data: PurchaseRequest):
    user = db.users.find_one({"phone_number": data.phone_number})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_points = user.get("loyalty_points", 0)

    # Validate user-supplied points
    if data.loyalty_points_to_use > current_points:
        raise HTTPException(status_code=400, detail="Not enough loyalty points")
    if data.loyalty_points_to_use < 0:
        raise HTTPException(status_code=400, detail="Invalid loyalty point value")

    discount = data.loyalty_points_to_use * 0.2
    final_amount = max(data.amount - discount, 0)

    # Deduct loyalty points
    db.users.update_one(
        {"_id": user["_id"]},
        {"$inc": {"loyalty_points": -data.loyalty_points_to_use}}
    )

    # Award new points
    points_earned = int(final_amount // 100) * 10
    db.users.update_one(
        {"_id": user["_id"]},
        {"$inc": {"loyalty_points": points_earned}}
    )

    db.purchases.insert_one({
        "phone_number": data.phone_number,
        "original_amount": data.amount,
        "loyalty_points_used": data.loyalty_points_to_use,
        "discount_applied": discount,
        "final_amount": final_amount,
        "points_earned": points_earned
    })

    return {
        "message": "Purchase successful",
        "used_loyalty_points": data.loyalty_points_to_use,
        "discount": discount,
        "amount_paid": final_amount,
        "points_earned": points_earned,
        "new_balance": current_points - data.loyalty_points_to_use + points_earned
    }
