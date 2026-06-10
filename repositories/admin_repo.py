from typing import List

from sqlalchemy.orm import Session
from models.models import Admin, SavingsAccount, Customer, Loan
from schemas.admin_schema import AdminCreate, AdminUpdate, SavingAccountAdmin, LoginRequest
from core.password import hash_password, verify_password
import uuid
from sqlalchemy.orm import joinedload
import random
import logging
from log_conf import init_logging


init_logging()

logger = logging.getLogger(__name__)

def random_account_administrator(db: Session):
    admins = db.query(Admin).filter(Admin.admin_role == "Account Administrator").all()
    if not admins:
        logger.warning("No account administrators found")
        return None
    
    return random.choice(admins)
def create_admin(db: Session, admin_data: AdminCreate):
    # check if admin already exists
    existing_admin = db.query(Admin).filter(Admin.email == admin_data.email).first()

    if existing_admin:
        logger.warning(f"Admin with email {admin_data.email} already exists")

        raise ValueError("Admin with this email already exists")

    # hash password
    hashed_password = hash_password(admin_data.password)

    new_admin = Admin(
        admin_role=admin_data.admin_role,
        admin_first_name=admin_data.admin_first_name,
        admin_last_name=admin_data.admin_last_name,
        email=admin_data.email,
        password=hashed_password
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    logger.info(f"Admin {new_admin.email} created successfully with ID {new_admin.admin_id}")
    return new_admin

def login_admin(db: Session, admin_data: LoginRequest):
    # find customer by email
    admin = db.query(Admin).filter(Admin.email == admin_data.email).first()

    if not admin:
        logger.warning(f"Login failed for email {admin_data.email}: Admin not found")
        raise ValueError("Invalid email or password")
        return None

    # verify password
    if not verify_password(admin_data.password, admin.password):
        logger.warning(f"Login failed for email {admin_data.email}: Incorrect password")
        raise ValueError("Invalid email or password")
        return None
    
    logger.info(f"Admin {admin.email} logged in successfully")
    return admin

def update_admin(db: Session, admin_id: uuid.UUID, admin_update: AdminUpdate):
    db_admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()

    if not db_admin:
        logger.warning(f"Attempted to update admin with ID {admin_id}, but admin was not found")
        raise ValueError("Admin not found")

    update_data = admin_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_admin, key, value)
    if "password" in update_data:
        db_admin.password = hash_password(update_data["password"])
    db.commit()
    db.refresh(db_admin)
    logger.info(f"Admin with ID {admin_id} updated successfully")
    return db_admin 

def delete_admin(db: Session, admin_id: uuid.UUID):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()

    if not admin:
        logger.warning(f"Attempted to delete admin with ID {admin_id}, but admin was not found")
        raise ValueError("Admin not found")
        
    db.delete(admin)
    db.commit()
    logger.info(f"Admin with ID {admin_id} deleted successfully")
    return admin
def get_admin_savings_accounts(db: Session, admin_id: uuid.UUID):


    accounts = (
        db.query(SavingsAccount)
        .join(SavingsAccount.customer)
        .filter(SavingsAccount.admin_id == admin_id)
        .all()
    )
    if not accounts:
        logger.info(f"No savings accounts found for admin")
        raise ValueError("No savings accounts found for this admin")
    result = []

    for account in accounts:
        result.append({
            "owner_id": str(account.customer_id),
            "owner_first_name": account.customer.first_name,
            "owner_last_name": account.customer.last_name,
            "balance": account.balance,
            "creation_date": account.created_date,
            "is_verified": account.is_verified
        })

    return result

def get_admin_unverified_savings_accounts(db: Session, admin_id: uuid.UUID):


    accounts = (
        db.query(SavingsAccount)
        .join(SavingsAccount.customer)
        .filter(SavingsAccount.admin_id == admin_id)
        .filter(SavingsAccount.is_verified == False)
        .all()
    )

    result = []

    for account in accounts:
        result.append({
            "owner_id": str(account.customer_id),
            "owner_first_name": account.customer.first_name,
            "owner_last_name": account.customer.last_name,
            "balance": account.balance,
            "creation_date": account.created_date,
            "is_verified": account.is_verified
        })

    return result




def delete_admin(db: Session, admin_id):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()

    if not admin:
        logger.warning(f"Attempted to delete admin with ID {admin_id}, but admin was not found")
        raise ValueError("Admin not found")

    db.delete(admin)
    db.commit()

    return admin

#def get_admin_savings_account(db:Session, admin_id: uuid.UUID):
#    return db.query(SavingsAccount).filter(SavingsAccount.admin_id== admin_id).all()

def admin_login(db: Session, admin_data: LoginRequest):
    # find customer by email
    customer = db.query(Admin).filter(Admin.email == admin_data.email).first()

    if not customer:
        logger.warning(f"Login failed for email {admin_data.email}: Admin not found")
        raise ValueError("Invalid email or password")
        return None

    # verify password
    if not verify_password(admin_data.password, admin_data.password):
        logger.warning(f"Login failed for email {admin_data.email}: Invalid password")
        raise ValueError("Invalid email or password")   
        return None

    return customer



def get_admin_loans(db: Session, admin_id: uuid.UUID):

    loans = (
        db.query(Loan)
        .options(joinedload(Loan.customer))
        .filter(Loan.admin_id == admin_id)
        .all()
    )
    if not loans:
        logger.info(f"No loans found for admin with ID {admin_id}")
        raise ValueError("No loans found for this admin")
    logger.info(f"{len(loans)} loan(s) found for admin with ID {admin_id}")
    return [
        {
            "owner_id": str(loan.customer_id),
            "owner_first_name": loan.customer.first_name if loan.customer else None,
            "owner_last_name": loan.customer.last_name if loan.customer else None,
            "loan_amount": loan.loan_amount,
            "loan_status": loan.loan_status,   # added
            "creation_date": loan.created_date,
            "time_of_closure": loan.time_of_closure,
            "is_verified": loan.is_verified
        }
        for loan in loans
    ]

def get_admin_unverified_loan(db: Session, admin_id: uuid.UUID):


    loans = (
        db.query(Loan)
        .join(Loan.customer)
        .filter(Loan.admin_id == admin_id)
        .filter(Loan.is_verified == False)
        .all()
    )
    if not loans:
        logger.info(f"No unverified loans found for admin with ID {admin_id}")
        raise ValueError("No unverified loans found for this admin")
    result = []

    for loan in loans:
        result.append({
            "owner_id": str(loan.customer_id),
            "owner_first_name": loan.customer.first_name,
            "owner_last_name": loan.customer.last_name,
            "loan_amount": loan.loan_amount,
            "creation_date": loan.created_date,
            "is_verified": loan.is_verified
        })
    logger.info(f"{len(result)} unverified loan(s) found for admin with ID {admin_id}")
    return result

def verify_account(db: Session, account_ids: List[uuid.UUID]):
    accounts = db.query(SavingsAccount).filter(SavingsAccount.account_id.in_(account_ids)).all()

    if not accounts:
        logger.warning(f"Attempted to verify accounts with IDs {account_ids}, but no accounts were found")
        raise ValueError("No accounts found with the provided IDs")

    for account in accounts:
        account.is_verified = True

    db.commit()
    logger.info(f"{len(accounts)} account(s) verified successfully with IDs: {[str(account.account_id) for account in accounts]}")
    return accounts

def verify_loan(db: Session, loan_ids: List[uuid.UUID]):
    loans = db.query(Loan).filter(Loan.loan_id.in_(loan_ids)).all()

    if not loans:
        logger.warning(f"Attempted to verify loans with IDs {loan_ids}, but no loans were found")
        raise ValueError("No loans found with the provided IDs")

    for loan in loans:
        loan.is_verified = True

    db.commit()
    logger.info(f"{len(loans)} loan(s) verified successfully with IDs: {[str(loan.loan_id) for loan in loans]}")
    return loans