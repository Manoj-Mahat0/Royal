from pydantic import BaseModel

class UserLogin(BaseModel):
    phone_number: str
    dob: str

class AddUser(BaseModel):
    full_name: str
    phone_number: str
    email: str           # ✅ NEW FIELD
    dob: str             # Format: YYYY-MM-DD
    role: str            # MAIN_STORE, SUB_STORE, FACTORY, etc.