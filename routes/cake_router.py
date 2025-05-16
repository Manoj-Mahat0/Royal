from datetime import datetime
from bson import ObjectId
from click import File
from fastapi import APIRouter, Body, Form, HTTPException, UploadFile
from database import db
from models.cake_order_model import CakeOrder, CakeQuantityUpdate, OrderStatusUpdate
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
    order_data = order.dict()
    cakes = order_data.get("cakes", [])

    total_price = 0
    enriched_cakes = []

    for cake in cakes:
        cake_name = cake.get("cake_name")

        for weight, qty in [(1, cake.get("quantity_1lbs", 0)),
                            (2, cake.get("quantity_2lbs", 0)),
                            (3, cake.get("quantity_3lbs", 0))]:
            if qty > 0:
                cake_entry = db.cake_names.find_one({
                    "name": cake_name,
                    "weight_lb": weight
                })

                if not cake_entry:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Cake not found: {cake_name} ({weight} lb)"
                    )

                unit_price = cake_entry["price"]
                subtotal = unit_price * qty
                total_price += subtotal

                enriched_cakes.append({
                    "cake_name": cake_name,
                    "weight_lb": weight,
                    "quantity": qty,
                    "unit_price": unit_price,
                    "subtotal": subtotal
                })

    if not enriched_cakes:
        raise HTTPException(status_code=400, detail="At least one valid cake quantity is required.")

    db.cake_orders.insert_one({
        "store_id": order_data["store_id"],
        "delivery_date": order_data["delivery_date"],
        "status": order_data.get("status", "PLACED"),
        "notes": order_data.get("notes", ""),
        "cakes": enriched_cakes,
        "total_price": total_price
    })

    return {
        "message": "Order placed successfully",
        "total_price": total_price
    }

@router.get("/cake/order/details")
def get_all_cake_order_details():
    orders = db.cake_orders.find()
    response = []

    for order in orders:
        # Get store name from store_id
        store_name = "Unknown Store"
        store_id = order.get("store_id")
        if store_id and ObjectId.is_valid(store_id):
            store = db.stores.find_one({"_id": ObjectId(store_id)})
            if store:
                store_name = store.get("name", "Unnamed Store")

        # Build cake details
        cake_items = []
        for cake in order.get("cakes", []):
            cake_items.append({
                "cake_name": cake.get("cake_name", ""),
                "weight_lb": cake.get("weight_lb", ""),
                "quantity": cake.get("quantity", ""),
                "unit_price": cake.get("unit_price", ""),
                "subtotal": cake.get("subtotal", "")
            })

        response.append({
            "_id": str(order["_id"]),
            "store_name": store_name,
            "delivery_date": order.get("delivery_date", ""),
            "status": order.get("status", ""),
            "notes": order.get("notes", ""),
            "cakes": cake_items,
            "total_price": order.get("total_price", 0)
        })

    return response

@router.patch("/cake/order/{order_id}/update-cake")
def update_cake_quantity(order_id: str, update: CakeQuantityUpdate):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")

    order = db.cake_orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated = False
    new_cakes = []

    for cake in order.get("cakes", []):
        if (cake.get("cake_name") == update.cake_name and 
            cake.get("weight_lb") == update.weight_lb):
            
            # Update quantity
            cake["quantity"] = update.new_quantity

            # Recalculate subtotal
            cake["subtotal"] = cake["unit_price"] * update.new_quantity

            # Add remarks
            cake["remarks"] = update.remarks

            updated = True

        new_cakes.append(cake)

    if not updated:
        raise HTTPException(status_code=404, detail="Matching cake not found in order")

    # Recalculate total price
    new_total = sum(c["subtotal"] for c in new_cakes)

    db.cake_orders.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "cakes": new_cakes,
                "total_price": new_total
            }
        }
    )

    return {
        "message": "Cake quantity and remarks updated successfully",
        "new_total_price": new_total
    }


@router.get("/options/cake-names")
def get_cake_names():
    cakes_cursor = db.cake_names.find({}, {"_id": 0, "name": 1, "weight_lb": 1, "price": 1})
    cakes = list(cakes_cursor)

    grouped = {}
    for cake in cakes:
        name = cake.get("name", "")
        if name not in grouped:
            grouped[name] = []
        grouped[name].append({
            "weight_lb": cake.get("weight_lb", 0),
            "price": cake.get("price", 0)
        })

    # Convert to desired list format
    result = [
        {
            "name": name,
            "variants": sorted(variants, key=lambda x: x["weight_lb"])
        }
        for name, variants in grouped.items()
    ]

    # Optional: sort alphabetically by name
    result.sort(key=lambda x: x["name"])

    return result



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

    total_quantity = sum(
        cake.quantity_1lbs + cake.quantity_2lbs + cake.quantity_3lbs
        for cake in order.cakes
    )

    if total_quantity == 0:
        raise HTTPException(status_code=400, detail="At least one cake must have quantity greater than 0")

    db.cake_orders.insert_one(order.dict())

    return {
        "message": "Multi-cake order placed successfully",
        "store_id": order.store_id,
        "status": order.status,
        "cakes": order.cakes
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
