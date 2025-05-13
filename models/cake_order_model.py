from pydantic import BaseModel
from typing import List

class CakeItem(BaseModel):
    cake_name: str
    quantity_1lbs: int = 0
    quantity_2lbs: int = 0
    quantity_3lbs: int = 0

class CakeOrder(BaseModel):
    store_id: str
    delivery_date: str  # YYYY-MM-DD
    status: str = "PLACED"
    notes: str = ""
    cakes: List[CakeItem]


class OrderStatusUpdate(BaseModel):
    status: str
    remarks: str = ""  # optional remarks field
