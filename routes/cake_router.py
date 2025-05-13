from datetime import datetime
from bson import ObjectId
from click import File
from fastapi import APIRouter, Body, Form, HTTPException, UploadFile
from database import db
from models.cake_order_model import CakeOrder, OrderStatusUpdate
import os

router = APIRouter()

@router.get("/options/bases")
def get_cake_bases():
    bases = db.cake_bases.find()
    return [b["name"] for b in bases]

@router.get("/options/flavors")
def get_flavors():
    flavors = db.flavors.find()
    return [f["name"] for f in flavors]

@router.get("/options/ingredients")
def get_ingredients():
    ingredients = db.ingredients.find()
    return [i["name"] for i in ingredients]

@router.get("/options/designs")
def get_designs():
    designs = db.designs.find()
    return [d["name"] for d in designs]

@router.post("/cake/order")
def place_order(order: CakeOrder):
    db.cake_orders.insert_one(order.dict())
    return {"message": "Order placed successfully"}

@router.get("/cake/orders/{phone}")
def get_orders(phone: str):
    orders = db.cake_orders.find({"phone_number": phone})
    return [ {**o, "_id": str(o["_id"])} for o in orders ]

@router.get("/orders")
def get_all_orders():
    orders = db.cake_orders.find()
    response = []

    for o in orders:
        store_name = "Unknown Store"
        store_id = o.get("store_id")

        # Handle valid ObjectId lookup
        if store_id and ObjectId.is_valid(store_id):
            try:
                store = db.stores.find_one({"_id": ObjectId(store_id)})
                if store:
                    store_name = store.get("name", "Unnamed Store")
            except:
                store_name = "Error Fetching Store"

        response.append({
            "_id": str(o["_id"]),
            "store_name": store_name,
            "cake_base": o.get("cake_base", ""),
            "flavor": o.get("flavor", ""),
            "ingredients": o.get("ingredients", []),
            "quantity": o.get("quantity", 1),
            "delivery_date": o.get("delivery_date", ""),
            "status": o.get("status", "PLACED"),
            "remarks": o.get("remarks", ""),
            # Optional fields if available (for customer-origin orders)
            "customer_name": o.get("customer_name", ""),
            "phone_number": o.get("phone_number", ""),
            "design": o.get("design", ""),
            "message_on_cake": o.get("message_on_cake", "")
        })

    return response


@router.post("/order")
def place_bulk_cake_order(order: CakeOrder):
    if not db.stores.find_one({"_id": ObjectId(order.store_id)}):
        raise HTTPException(status_code=404, detail="Store not found")

    total_quantity = order.quantity_1lbs + order.quantity_2lbs + order.quantity_3lbs
    if total_quantity == 0:
        raise HTTPException(status_code=400, detail="At least one quantity must be greater than 0")

    db.cake_orders.insert_one(order.dict())

    return {
        "message": f"Cake order for '{order.cake_name}' placed by store",
        "status": order.status,
        "store_id": order.store_id,
        "quantities": {
            "1lbs": order.quantity_1lbs,
            "2lbs": order.quantity_2lbs,
            "3lbs": order.quantity_3lbs
        }
    }


@router.patch("/order/{order_id}/status")
def update_order_status(order_id: str, update: OrderStatusUpdate):
    valid_statuses = ["PLACED", "CONFIRMED", "BAKING", "READY", "DELIVERED", "CANCELLED"]

    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from {valid_statuses}")

    update_data = {"status": update.status}
    if update.remarks:
        update_data["remarks"] = update.remarks

    result = db.cake_orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": f"Order status updated to '{update.status}'", "remarks": update.remarks}

@router.get("/orders/status")
def get_all_order_statuses():
    orders = db.cake_orders.find()
    response = []

    for o in orders:
        store_name = "Unknown Store"
        store_id = o.get("store_id", "")
        if store_id:
            try:
                store = db.stores.find_one({"_id": ObjectId(store_id)})
                if store:
                    store_name = store["name"]
            except:
                pass

        response.append({
            "order_id": str(o["_id"]),
            "store_name": store_name,
            "status": o.get("status", "PLACED")
        })

    return response

@router.post("/design/upload")
async def upload_cake_design(
    # Design metadata
    
    image: UploadFile = File(...),

    # Cake order fields
    store_id: str = Form(...),
    cake_base: str = Form(...),
    flavor: str = Form(...),
    ingredients: str = Form(...),  # comma-separated
    quantity: int = Form(...),
    delivery_date: str = Form(...),
    status: str = Form("PLACED"),
    notes: str = Form("")
):
    # Validate store ID
    if not db.stores.find_one({"_id": ObjectId(store_id)}):
        return {"error": "Invalid store_id"}

    # Save image
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ext = image.filename.split(".")[-1]
    filename = f"{store_id.replace(' ', '_')}_{timestamp}.{ext}"
    save_path = os.path.join("uploads", "designs", filename)
    with open(save_path, "wb") as f:
        f.write(await image.read())

    # Save to DB
    db.cake_designs.insert_one({
        "image_path": save_path,
        "uploaded_at": datetime.utcnow(),
        "cake_details": {
            "store_id": store_id,
            "cake_base": cake_base,
            "flavor": flavor,
            "ingredients": [i.strip() for i in ingredients.split(",") if i.strip()],
            "quantity": quantity,
            "delivery_date": delivery_date,
            "status": status,
            "notes": notes
        }
    })

    return {
        "message": "Cake design with order info uploaded successfully",
        "filename": filename
    }

@router.get("/designs")
def get_all_cake_designs():
    designs = db.cake_designs.find()
    response = []

    for d in designs:
        store_name = "Unknown Store"
        store_id = d.get("cake_details", {}).get("store_id", "")

        if store_id and ObjectId.is_valid(store_id):
            try:
                store = db.stores.find_one({"_id": ObjectId(store_id)})
                if store:
                    store_name = store.get("name", "Unnamed Store")
            except:
                store_name = "Error Fetching Store"

        response.append({
            "_id": str(d["_id"]),
            "image_path": d.get("image_path", ""),
            "uploaded_at": d.get("uploaded_at", ""),
            "store_name": store_name,
            "cake_base": d.get("cake_details", {}).get("cake_base", ""),
            "flavor": d.get("cake_details", {}).get("flavor", ""),
            "ingredients": d.get("cake_details", {}).get("ingredients", []),
            "quantity": d.get("cake_details", {}).get("quantity", 1),
            "delivery_date": d.get("cake_details", {}).get("delivery_date", ""),
            "status": d.get("cake_details", {}).get("status", "PLACED"),
            "notes": d.get("cake_details", {}).get("notes", "")
        })

    return response
