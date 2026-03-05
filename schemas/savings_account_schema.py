from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone
from pydantic import BaseModel, EmailStr
import uuid
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID

class EmploymentCreate(BaseModel):
    employer_first_name: str
    customer_id: int
    balance: Decimal
    job_title: str
    admin_id: int
    is_verified: bool
