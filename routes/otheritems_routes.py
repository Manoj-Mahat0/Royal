from fastapi import APIRouter, Body, Depends, HTTPException
from database import db
from bson import ObjectId

from utils.auth_dependencies import get_current_user_rolewise

router = APIRouter()

# ---- Snacks ----
@router.post("/snacks/add")
def add_snack(
    name: str = Body(...),
    price: float = Body(...),
    user=Depends(get_current_user_rolewise)
):
    # Only allow certain roles if needed, e.g.:
    # if user["role"] != "admin":
    #     raise HTTPException(status_code=403, detail="Not authorized")
    snack = {"name": name, "price": price}
    result = db.snacks.insert_one(snack)
    return {"message": "Snack added", "_id": str(result.inserted_id)}

@router.get("/snacks")
def get_snacks():
    snacks = db.snacks.find()
    return [{"_id": str(s["_id"]), "name": s.get("name", ""), "price": s.get("price", 0)} for s in snacks]

# ---- Pastries ----
@router.post("/pastries/add")
def add_pastry(name: str = Body(...), price: float = Body(...)):
    pastry = {"name": name, "price": price}
    result = db.pastries.insert_one(pastry)
    return {"message": "Pastry added", "_id": str(result.inserted_id)}

@router.get("/pastries")
def get_pastries():
    pastries = db.pastries.find()
    return [{"_id": str(p["_id"]), "name": p.get("name", ""), "price": p.get("price", 0)} for p in pastries]

# ---- Edit Snack ----
@router.put("/snacks/{snack_id}")
def edit_snack(
    snack_id: str,
    name: str = Body(...),
    price: float = Body(...),
    user=Depends(get_current_user_rolewise)
):
    if not ObjectId.is_valid(snack_id):
        raise HTTPException(status_code=400, detail="Invalid snack ID")
    result = db.snacks.update_one(
        {"_id": ObjectId(snack_id)},
        {"$set": {"name": name, "price": price}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Snack not found")
    return {"message": "Snack updated"}

# ---- Delete Snack ----
@router.delete("/snacks/{snack_id}")
def delete_snack(
    snack_id: str,
    user=Depends(get_current_user_rolewise)
):
    if not ObjectId.is_valid(snack_id):
        raise HTTPException(status_code=400, detail="Invalid snack ID")
    result = db.snacks.delete_one({"_id": ObjectId(snack_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Snack not found")
    return {"message": "Snack deleted"}

# ---- Edit Pastry ----
@router.put("/pastries/{pastry_id}")
def edit_pastry(
    pastry_id: str,
    name: str = Body(...),
    price: float = Body(...),
    user=Depends(get_current_user_rolewise)
):
    if not ObjectId.is_valid(pastry_id):
        raise HTTPException(status_code=400, detail="Invalid pastry ID")
    result = db.pastries.update_one(
        {"_id": ObjectId(pastry_id)},
        {"$set": {"name": name, "price": price}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pastry not found")
    return {"message": "Pastry updated"}

# ---- Delete Pastry ----
@router.delete("/pastries/{pastry_id}")
def delete_pastry(
    pastry_id: str,
    user=Depends(get_current_user_rolewise)
):
    if not ObjectId.is_valid(pastry_id):
        raise HTTPException(status_code=400, detail="Invalid pastry ID")
    result = db.pastries.delete_one({"_id": ObjectId(pastry_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pastry not found")
    return {"message": "Pastry deleted"}