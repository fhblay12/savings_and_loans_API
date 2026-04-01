



from decimal import Decimal
import uuid

from fastapi import APIRouter, Depends
from requests import Session

from database import get_db
from models.models import Loan, LoanPayment
from services.customer_loan_payment_services import standard_loan_payment


router = APIRouter(prefix="/loan_payments", tags=["Loan Payments"])

@router.post("/{customer_id}/loan_payment")
def loan_payment(
    loan_id: uuid.UUID,
    payment_amount: float,
    payment_type: str,
    db: Session = Depends(get_db)
):

    payment_amount = Decimal(str(payment_amount))
    payment_type=payment_type.capitalize()
    loan = (
        db.query(Loan)
        .filter(Loan.loan_id == loan_id)
        .first()
    )

    if not loan:
        raise ValueError("Loan not found")

    # Update balance correctly
    if payment_type == "Standard":
        standard_loan_payment(loan, payment_amount) 

    else:
        raise ValueError("Invalid transaction type")

    # Create transaction record
    payment = LoanPayment(
        loan_id=loan_id,
        payment_amount=payment_amount,
        payment_type=payment_type,
        
    )

    db.add(payment)

    # Commit BOTH changes together
    db.commit()
    db.refresh(loan)

    return loan

@router.get("/{loan_id}/loan_payment")
def get_loan_payment(payment_id: uuid.UUID, db: Session = Depends(get_db )):
    payments = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).all()
    return { "payments": payments }

@router.delete("/loan_payment/{payment_id}")
def delete_loan_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(LoanPayment).filter(LoanPayment.payment_id == payment_id).first()
    if not payment:
        raise ValueError("Payment not found")
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}

@router.patch("/loan_payment/{payment_id}")
def update_loan_payment(loan_payment_id: uuid.UUID, payment_amount: float, db: Session = Depends(get_db)):
    payment = db.query(LoanPayment).filter(LoanPayment.loan_payment_id == loan_payment_id).first()
    if not payment:
        raise ValueError("Payment not found")
    payment.payment_amount = Decimal(str(payment_amount))
    db.commit()
    db.refresh(payment)
    return payment