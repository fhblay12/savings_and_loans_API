from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.loan_schema import LoanCreate, LoanUpdate, loan_form
from schemas.collateral_schema import Collateral_schema, collateral_form
from repositories.loan_repo import create_loan_details, create_collateral, get_loan_by_id, update_loan_details
from repositories.admin_repo import random_account_administrator
from repositories.collateral_repo import create_collateral_details
from core.security import create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from core.password import hash_password, verify_password
from models.models import Loan, Admin, Collateral
from database import get_db
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
import random
import uuid
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/loan", tags=["loan"])

# @router.get("/apply/{customer_id}", response_class=HTMLResponse)
# def show_apply_form(request: Request, customer_id: uuid.UUID):
#     return templates.TemplateResponse(
#         "apply_loan.html",
#         {
#             "request": request,
#             "customer_id": customer_id
#         }
#     )

@router.post("/apply/{customer_id}")
def apply_loan(
    request: Request,
    customer_id: uuid.UUID,
    loan: LoanCreate,
    db: Session = Depends(get_db)
):
        # Pick a random account administrator
    try:
        admin = random_account_administrator(db)
    except Exception as e:
        return{"request": request, "error": str(e)}
        
    #toc = loan_data.created_date + relativedelta(months=loan_data.loan_term)
    new_loan = create_loan_details(db, loan, admin, customer_id)

    return{
            "message": "Loan application submitted successfully",
            "loan": new_loan
        }

@router.patch("/update/{loan_id}")
def update_loan(loan_id: uuid.UUID, loan_update: LoanUpdate, db: Session = Depends(get_db)):
    try:
        updated_loan = update_loan_details(db=db, loan_id=loan_id, loan_update=loan_update)
        return updated_loan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete/{loan_id}")
def delete_loan(loan_id: uuid.UUID, db: Session = Depends(get_db)): 
    try:
        loan = delete_loan(db, loan_id)
        return {"message": "Loan deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{loan_id}")
def get_loan(loan_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        loan = get_loan_by_id(db, loan_id)
        return loan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
