from sqlalchemy.orm import Session
from models.models import Admin, SavingsAccount, Customer, Loan
from schemas.admin_schema import AdminCreate, SavingAccountAdmin, LoginRequest
from core.password import hash_password, verify_password
import uuid


def create_admin(db: Session, admin_data: AdminCreate):
    # check if admin already exists
    existing_admin = db.query(Admin).filter(Admin.email == admin_data.email).first()

    if existing_admin:
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

    return new_admin


def get_admin_savings_accounts(db: Session, admin_id: uuid.UUID):


    accounts = (
        db.query(SavingsAccount)
        .join(SavingsAccount.customer)
        .filter(SavingsAccount.admin_id == admin_id)
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

def get_admin_unverified_savings_accounts(db: Session, admin_id: uuid.UUID):


    accounts = (
        db.query(SavingsAccount)
        .join(SavingsAccount.customer)
        .filter(SavingsAccount.admin_id == admin_id)
        .filter(SavingsAccount.is_verified == 0)
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


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


def get_admin_by_id(db: Session, admin_id):
    return db.query(Admin).filter(Admin.admin_id == admin_id).first()


def get_all_admins(db: Session):
    return db.query(Admin).all()


def delete_admin(db: Session, admin_id):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()

    if not admin:
        return None

    db.delete(admin)
    db.commit()

    return admin

#def get_admin_savings_account(db:Session, admin_id: uuid.UUID):
#    return db.query(SavingsAccount).filter(SavingsAccount.admin_id== admin_id).all()

def admin_login(db: Session, admin_data: LoginRequest):
    # find customer by email
    customer = db.query(Admin).filter(Admin.email == admin_data.email).first()

    if not customer:
        return None

    # verify password
    if not verify_password(admin_data.password, admin_data.password):
        return None

    return customer




def get_admin_loans(db: Session, admin_id: uuid.UUID):


    loans = (
        db.query(Loan)
        .join(Loan.customer)
        .filter(Loan.admin_id == admin_id)
        .all()
    )

    result = []

    for account in loans:
        result.append({
            "owner_id": str(loans.customer_id),
            "owner_first_name": loans.customer.first_name,
            "owner_last_name": loans.customer.last_name,
            "loan_amount": loans.loan_amount,
            "creation_date": loans.created_date,
            "is_verified": loans.is_verified
        })

    return result


def get_admin_unverified_savings_accounts(db: Session, admin_id: uuid.UUID):


    loans = (
        db.query(Loan)
        .join(Loan.customer)
        .filter(Loan.admin_id == admin_id)
        .filter(Loan.is_verified == 0)
        .all()
    )

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

    return result