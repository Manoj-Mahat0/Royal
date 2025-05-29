from fastapi import APIRouter, Query
from database import db

router = APIRouter()

@router.get("/analytics/orders")
def get_order_analytics(store_id: str = Query(None)):
    # Filter orders by store_id if provided
    query = {}
    if store_id:
        query["store_id"] = store_id

    orders = list(db.cake_orders.find(query))
    stores = {str(store["_id"]): store.get("name", "Unknown Store") for store in db.stores.find()}
    shop_analytics = {}

    for order in orders:
        store_id_val = str(order.get("store_id", ""))
        store_name = stores.get(store_id_val, "Unknown Store")
        order_date = ""
        order_time = ""
        if "created_at" in order:
            created_at = order["created_at"]
            if hasattr(created_at, "strftime"):
                order_date = created_at.strftime("%Y-%m-%d")
                order_time = created_at.strftime("%H:%M:%S")
            else:
                order_date = str(created_at)[:10]
                order_time = str(created_at)[11:19]

        if store_name not in shop_analytics:
            shop_analytics[store_name] = {
                "total_orders": 0,
                "total_revenue": 0,
                "orders_by_status": {},
                "top_cakes_counter": {},
                "orders": []
            }

        shop = shop_analytics[store_name]
        shop["total_orders"] += 1
        shop["total_revenue"] += order.get("total_price", 0)

        # Orders by status
        status = order.get("status", "UNKNOWN")
        shop["orders_by_status"][status] = shop["orders_by_status"].get(status, 0) + 1

        # Top cakes by quantity
        for cake in order.get("cakes", []):
            key = f"{cake.get('cake_name', '')} ({cake.get('weight_lb', '')} lb)"
            shop["top_cakes_counter"][key] = shop["top_cakes_counter"].get(key, 0) + cake.get("quantity", 0)

        # Add order date and time for each order
        shop["orders"].append({
            "order_id": str(order["_id"]),
            "date": order_date,
            "time": order_time,
            "total_price": order.get("total_price", 0),
            "status": status
        })

    # Prepare final analytics
    result = []
    for store_name, data in shop_analytics.items():
        top_cakes = sorted(data["top_cakes_counter"].items(), key=lambda x: x[1], reverse=True)[:5]
        result.append({
            "store_name": store_name,
            "total_orders": data["total_orders"],
            "total_revenue": data["total_revenue"],
            "orders_by_status": data["orders_by_status"],
            "top_5_cakes": [{"cake": name, "quantity": qty} for name, qty in top_cakes],
            "orders": data["orders"]  # includes date and time for each order
        })

    return result