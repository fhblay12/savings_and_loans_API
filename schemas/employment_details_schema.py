from typing import Optional

from pydantic import BaseModel, EmailStr, AwareDatetime
from datetime import date, timezone
from pydantic import BaseModel, EmailStr
import uuid
from sqlalchemy.dialects.postgresql import UUID

class EmploymentCreate(BaseModel):
    employer_first_name: str
    employer_last_name: str
    customer_id: uuid.UUID
    job_title: str
    employment_type: str
    monthly_income: int
    employment_start_date: date

class EmploymentUpdate(BaseModel):
    employer_first_name: Optional[str] = None
    employer_last_name: Optional[str] = None
    customer_id: Optional[uuid.UUID] = None
    job_title: Optional[str] = None
    employment_type: Optional[str] = None
    monthly_income: Optional[int] = None
    employment_start_date: Optional[date] = None