



from decimal import Decimal
import uuid

from fastapi import APIRouter, Depends
from requests import Session

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
    db: Session = Depends(get_db)
):
    new_payment=create_loan_payment(db, loan_payment_data)
    return new_payment

@router.get("/{loan_id}/loan_payments")
def get_loan_payment(loan_id: uuid.UUID, db: Session = Depends(get_db )):
    payments = get_loan_payments_by_loan(db, loan_id)
    return { "payments": payments }

@router.delete("/loan_payment/{payment_id}")
def delete_loan_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = delete_loan_payment(db, payment_id)
    return {"message": "Payment deleted successfully"}

@router.patch("/loan_payment/{payment_id}")
def update_loan_payment(loan_payment_id: uuid.UUID, payment_amount: float, db: Session = Depends(get_db)):
    payment = update_loan_payment(db, loan_payment_id, payment_amount)
    return payment