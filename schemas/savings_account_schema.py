from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class SavingsAccountCreate(BaseModel):
    customer_id: uuid.UUID
    balance: Decimal
    admin_id: int
    is_verified: bool
