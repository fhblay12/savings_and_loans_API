from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional

class SavingsAccountCreate(BaseModel):
    customer_id: uuid.UUID
    balance: Decimal
    admin_id: uuid.UUID
    is_verified: Optional[bool] = False

class SavingsAccountResponse(BaseModel):
    customer_id: uuid.UUID
    balance: Decimal
    created_date: datetime
    class Config:
        from_attributes = True
    