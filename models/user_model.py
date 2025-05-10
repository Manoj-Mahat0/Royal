from pydantic import BaseModel

class UserLogin(BaseModel):
    phone_number: str
    dob: str

class AddUser(BaseModel):
    full_name: str
    phone_number: str
    dob: str  # format: YYYY-MM-DD
    role: str  # MAIN_STORE, SUB_STORE, FACTORY