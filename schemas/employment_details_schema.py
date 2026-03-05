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
