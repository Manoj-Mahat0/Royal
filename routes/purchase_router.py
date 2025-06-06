from fastapi import APIRouter, Body, HTTPException, Query
from models.purchase_model import PurchaseRequest
from database import db

router = APIRouter()

@router.post("/")
def handle_purchase(data: PurchaseRequest):
    user = db.users.find_one({"phone_number": data.phone_number})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_points = user.get("loyalty_points", 0)

    # Disallow using loyalty points if amount is < 500
    if data.amount < 500 and data.loyalty_points_to_use > 0:
        raise HTTPException(status_code=400, detail="Cannot use loyalty points for purchases below ₹500")

    # Validate usage
    if data.loyalty_points_to_use > current_points:
        raise HTTPException(status_code=400, detail="Not enough loyalty points")
    if data.loyalty_points_to_use < 0:
        raise HTTPException(status_code=400, detail="Invalid loyalty point value")

    discount = data.loyalty_points_to_use * 0.2
    final_amount = max(data.amount - discount, 0)

    # Deduct used points
    db.users.update_one(
        {"_id": user["_id"]},
        {"$inc": {"loyalty_points": -data.loyalty_points_to_use}}
    )

    # Only award points if final_amount ≥ 500 AND product is BAKERY or NOT
    points_earned = 0
    if final_amount >= 500 and data.product_type.upper() == "BAKERY":
        points_earned = int(final_amount // 100) * 10
        db.users.update_one(
            {"_id": user["_id"]},
            {"$inc": {"loyalty_points": points_earned}}
        )

    db.purchases.insert_one({
        "phone_number": data.phone_number,
        "original_amount": data.amount,
        "product_type": data.product_type,
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

@router.get("/loyalty-points")
def get_loyalty_points(phone_number: str = Query(..., description="User's phone number")):
    user = db.users.find_one({"phone_number": phone_number})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "full_name": user.get("full_name", ""),
        "phone_number": user["phone_number"],
        "loyalty_points": user.get("loyalty_points", 0)
    }

@router.put("/loyalty-points")
def update_loyalty_points(phone_number: str = Body(...), loyalty_points: int = Body(...)):
    result = db.users.update_one(
        {"phone_number": phone_number},
        {"$set": {"loyalty_points": loyalty_points}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "phone_number": phone_number,
        "loyalty_points": loyalty_points,
        "message": "Loyalty points updated"
    }