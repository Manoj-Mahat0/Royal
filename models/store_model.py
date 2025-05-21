from pydantic import BaseModel, Field

class StoreCreate(BaseModel):
    name: str
    type: str  # MAIN_STORE, SUB_STORE, or FACTORY
    phone_number: str = Field(..., min_length=10, max_length=15)
    dob: str  # in YYYY-MM-DD format
    latitude: float
    longitude: float

