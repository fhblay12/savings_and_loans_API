



from decimal import Decimal
import uuid

from fastapi import APIRouter, Depends
from requests import Session

from core.security import get_current_user
from database import get_db
from models.models import Loan, LoanPayment
from schemas.loan_payment_schema import LoanPayments
from services.customer_loan_payment_services import standard_loan_payment
from repositories.loan_payment_repo import create_loan_payment, get_loan_payment, get_loan_payments_by_loan, delete_loan_payment, update_loan_payment


router = APIRouter(prefix="/loan_payments", tags=["Loan Payments"])

@router.post("/{customer_id}/loan_payment")
def loan_payment(
    loan_id: uuid.UUID,
    loan_payment_data: LoanPayments,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_payment=create_loan_payment(db=db, loan_payment_data=loan_payment_data, loan_id=loan_id)
    return new_payment

@router.get("/{loan_id}/loan_payments_by_loan")
def get_loan_payment_by_loan(loan_id: uuid.UUID, db: Session = Depends(get_db ), current_user = Depends(get_current_user)):
    payments = get_loan_payments_by_loan(db=db, loan_id=loan_id)
    return { "payments": payments }

@router.get("/{payment_id}")
def get_loan_payment_by_id(payment_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    payment = get_loan_payment(payment_id=payment_id, db=db)
    return payment

@router.delete("/loan_payment/{payment_id}")
def delete_loan_payments(payment_id: uuid.UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    payment = delete_loan_payment(db=db, payment_id=payment_id)
    return {"message": "Payment deleted successfully"}

@router.patch("/loan_payment/{payment_id}")
def update_loan_payments(loan_payment_id: uuid.UUID, payment_amount: float, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    payment = update_loan_payment(db=db, payment_id=loan_payment_id, loan_payment_data=LoanPayments(payment_amount=payment_amount))
    return payment