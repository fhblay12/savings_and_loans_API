from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone, datetime
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
from fastapi import Depends, Form

class Collateral_schema(BaseModel):
    collateral_type: str
    collateral_value: str

def collateral_form(
    collateral_type: str = Form(...),
    collateral_value: str = Form(...)
) -> Collateral_schema:
    return Collateral_schema(
        collateral_type=collateral_type,
        collateral_value=collateral_value
    )