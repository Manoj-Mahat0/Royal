from pydantic import BaseModel

class PurchaseRequest(BaseModel):
    phone_number: str
    amount: float
    loyalty_points_to_use: int  # user input
