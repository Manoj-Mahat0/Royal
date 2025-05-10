from pydantic import BaseModel
from typing import List

class CakeOrder(BaseModel):
    store_id: str               # ID of the store placing the order
    cake_base: str              # e.g., Sponge, Butter
    flavor: str                 # e.g., Vanilla, Chocolate
    ingredients: List[str]      # list of ingredients requested
    quantity: int               # how many cakes requested
    delivery_date: str          # format: YYYY-MM-DD
    status: str = "PLACED"      # default status
    notes: str = ""             # optional message/notes


class OrderStatusUpdate(BaseModel):
    status: str
    remarks: str = ""  # optional remarks field
