from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class AdminCreate(BaseModel):
    admin_role: str
    admin_first_name: str
    admin_last_name: str
    password: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SavingAccountAdmin(BaseModel):
    owner_id:str
    owner_first_name:str
    owner_last_name:str
    balance: int
    creation_date: datetime
    is_verified: bool
    class Config:
        from_attributes = True

class LoanAdmin(BaseModel):
    owner_id:str
    owner_first_name:str
    owner_last_name:str
    loan_amount: int
    creation_date: datetime
    is_verified: bool
    time_of_closure: datetime
    class Config:
        from_attributes = True