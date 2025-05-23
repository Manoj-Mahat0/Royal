#cake_order_model
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class CakeItem(BaseModel):
    cake_name: str
    quantity_1lbs: int = 0
    quantity_2lbs: int = 0
    quantity_3lbs: int = 0

class CakeOrder(BaseModel):
    store_id: str
    delivery_date: str  # Format: YYYY-MM-DD
    status: str = "PLACED"
    notes: str = ""
    cakes: List[CakeItem]

class OrderStatusUpdate(BaseModel):
    status: str
    remarks: str = ""  # optional remarks field

class CakeQuantityUpdate(BaseModel):
    cake_name: str
    weight_lb: int
    new_quantity: int
    remarks: Optional[str] = ""

class DesignStatusUpdate(BaseModel):
    status: str
    remarks: str = ""  # optional

#--------------------------------------------#
class CakeOrderModel(BaseModel):
    user_id: str
    store_id: str
    store_name: str
    flavor: str
    weight: str
    price: float
    message_on_cake: Optional[str] = ""
    status: Optional[str] = "PLACED"
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)