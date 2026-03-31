from typing import Optional

from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone
from pydantic import BaseModel, EmailStr
from fastapi import Depends, Form

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    address: str
    social_security_number: str
    government_ID: Optional[str] = None
    email: EmailStr
    phone_number: str
    DOB: date
    credit_score: int
    customer_type: Optional[str] = None
    password: str

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    social_security_number: Optional[str] = None
    government_ID: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    DOB: Optional[date] = None
    credit_score: Optional[int] = None
    customer_type: Optional[str] = None
    password: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True

def customer_form(
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    social_security_number: str = Form(...),
    government_ID: str = Form(...),
    email: EmailStr = Form(...),
    phone_number: str = Form(...),
    DOB: date = Form(...),
    credit_score: int = Form(...),
    customer_type: str = Form(...),
    password: str = Form(...),
) -> CustomerCreate:
    return CustomerCreate(
        first_name=first_name,
        last_name=last_name,
        address=address,
        social_security_number=social_security_number,
        government_ID=government_ID,
        email=email,
        phone_number=phone_number,
        DOB=DOB,
        credit_score=credit_score,
        customer_type=customer_type,
        password=password
    )