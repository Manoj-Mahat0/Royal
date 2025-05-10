from pydantic import BaseModel

class StoreCreate(BaseModel):
    name: str
    type: str  # MAIN_STORE, SUB_STORE, or FACTORY
    location: str
    address: str
    phone_number: str
    dob: str  # in YYYY-MM-DD format

