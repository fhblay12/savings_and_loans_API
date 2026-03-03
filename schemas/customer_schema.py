from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    address: str
    social_security_number: str
    government_ID: str
    email: EmailStr
    phone_number: str
    DOB: date
    credit_score: int
    customer_type: str
  

class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True