from typing import Optional
import datetime
import decimal
from sqlalchemy.sql import func
from sqlalchemy import ARRAY, BigInteger, Boolean, Date, DateTime, ForeignKeyConstraint, Integer, LargeBinary, Numeric, PrimaryKeyConstraint, REAL, String, Text, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = 'admin'


    admin_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    admin_role: Mapped[str] = mapped_column(String, nullable=False)
    admin_first_name: Mapped[str] = mapped_column(String, nullable=False)       
    admin_last_name: Mapped[str] = mapped_column(String, nullable=False)        
    password : Mapped[String]= mapped_column(String(255), nullable=False)
    loan: Mapped[list['Loan']] = relationship('Loan', back_populates='admin')
    email: Mapped[str] = mapped_column(String(255), nullable=False)   

class Customer(Base):
    __tablename__ = 'customer'



    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    government_ID: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    credit_score: Mapped[int] = mapped_column(BigInteger, nullable=False)

    #created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    #updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))

    social_security_number: Mapped[Optional[str]] = mapped_column(String(20))
    proof_of_residence: Mapped[Optional[bytes]] = mapped_column(LargeBinary)

    DOB: Mapped[Optional[datetime.date]] = mapped_column(Date)
    customer_type: Mapped[Optional[str]] = mapped_column(String)
    password : Mapped[String]= mapped_column(String(255), nullable=False)
    employment_details: Mapped[list['EmploymentDetails']] = relationship(
        'EmploymentDetails', back_populates='customer'
    )
    loan: Mapped[list['Loan']] = relationship(
        'Loan', back_populates='customer'
    )
    savings_account: Mapped[list['SavingsAccount']] = relationship(
        'SavingsAccount', back_populates='customer'
    )


class PlayingWithNeon(Base):
    __tablename__ = 'playing_with_neon'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='playing_with_neon_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[Optional[float]] = mapped_column(REAL)


class EmploymentDetails(Base):
    __tablename__ = 'employment_details'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], name='employment_details_customer_id_fk'),
        PrimaryKeyConstraint('employment_details_id', name='employment_details_pkey')
    )

    employment_details_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[uuid.UUID] = mapped_column(Integer, nullable=False)
    job_title: Mapped[str] = mapped_column(String, nullable=False)
    employment_type: Mapped[str] = mapped_column(String, nullable=False)        
    monthly_income: Mapped[int] = mapped_column(Integer, nullable=False)        
    employment_start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    created_time: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    employer_first_name: Mapped[Optional[str]] = mapped_column(String)
    employer_last_name: Mapped[Optional[str]] = mapped_column(String)
    updated_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    customer: Mapped['Customer'] = relationship('Customer', back_populates='employment_details')


class Loan(Base):
    __tablename__ = 'loan'
    __table_args__ = (
        ForeignKeyConstraint(['admin_id'], ['admin.admin_id'], name='loan_admin_id_fk'),
        ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], name='loan_customer_id_fk'),
        PrimaryKeyConstraint('loan_id', name='loan_pkey')
    )

    loan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    loan_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(1000, 1000), nullable=False)
    term_in_months: Mapped[int] = mapped_column(Integer, nullable=False)
    admin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    loan_type: Mapped[str] = mapped_column(String, nullable=False)
    loan_status: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    time_of_closure: Mapped[Optional[datetime.date]] = mapped_column(Date)      
    noc: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    admin: Mapped['Admin'] = relationship('Admin', back_populates='loan')       
    customer: Mapped['Customer'] = relationship('Customer', back_populates='loan')
    collateral: Mapped[list['Collateral']] = relationship('Collateral', back_populates='loan')
    loan_interest: Mapped[list['LoanInterest']] = relationship('LoanInterest', back_populates='loan')
    loan_payment: Mapped[list['LoanPayment']] = relationship('LoanPayment', back_populates='loan')


class SavingsAccount(Base):
    __tablename__ = 'savings_account'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], name='savings_account_customer_id_fk'),
        PrimaryKeyConstraint('account_id', name='savings_account_pkey')
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    admin_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    balance: Mapped[decimal.Decimal] = mapped_column(Numeric(1000, 1000), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_date: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True), server_default=func.now()
    )

    updated_date: Mapped[datetime.datetime] = mapped_column(
    DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    customer: Mapped['Customer'] = relationship('Customer', back_populates='savings_account')
    savings_interest: Mapped[list['SavingsInterest']] = relationship('SavingsInterest', back_populates='account')
    transactions: Mapped[list['Transactions']] = relationship('Transactions', back_populates='account')

class Collateral(Base):
    __tablename__ = 'collateral'
    __table_args__ = (
        ForeignKeyConstraint(['loan_id'], ['loan.loan_id'], name='collateral_loan_id_fk'),
        PrimaryKeyConstraint('collateral_id', name='collateral_pkey')
    )

    collateral_id: Mapped[int] = mapped_column(Integer, primary_key=True)       
    loan_id: Mapped[int] = mapped_column(Integer, nullable=False)
    collateral_type: Mapped[str] = mapped_column(String, nullable=False)        
    collateral_value: Mapped[decimal.Decimal] = mapped_column(Numeric(1000, 1000), nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    loan: Mapped['Loan'] = relationship('Loan', back_populates='collateral')    


class LoanInterest(Base):
    __tablename__ = 'loan_interest'
    __table_args__ = (
        ForeignKeyConstraint(['loan_id'], ['loan.loan_id'], name='loan_interest_loan_id_fk'),
        PrimaryKeyConstraint('interest_id', name='loan_interest_pkey')
    )

    interest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    loan_id: Mapped[int] = mapped_column(Integer, nullable=False)
    interest_rate: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 10), nullable=False)
    effective_year: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    loan: Mapped['Loan'] = relationship('Loan', back_populates='loan_interest') 


class LoanPayment(Base):
    __tablename__ = 'loan_payment'
    __table_args__ = (
        ForeignKeyConstraint(['loan_id'], ['loan.loan_id'], name='loan_payment_loan_id_fk'),
        PrimaryKeyConstraint('loan_payment_id', name='loan_payment_pkey')       
    )

    loan_payment_id: Mapped[int] = mapped_column(Integer, primary_key=True)     
    loan_id: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(1000, 1000), nullable=False)
    payment_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)   
    payment_type: Mapped[int] = mapped_column(Integer, nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    loan: Mapped['Loan'] = relationship('Loan', back_populates='loan_payment')  


class SavingsInterest(Base):
    __tablename__ = 'savings_interest'
    __table_args__ = (
        ForeignKeyConstraint(['account_id'], ['savings_account.account_id'], name='savings_interest_account_id'),
        PrimaryKeyConstraint('interest_id', name='savings_interest_pkey')       
    )

    interest_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    apy: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 1000), nullable=False)
    year: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    account: Mapped['SavingsAccount'] = relationship('SavingsAccount', back_populates='savings_interest')


class Transactions(Base):
    __tablename__ = 'transactions'
    __table_args__ = (
        ForeignKeyConstraint(['account_id'], ['savings_account.account_id'], name='transactions_account_id_fk'),
        PrimaryKeyConstraint('transaction_id', 'transaction_type', name='transactions_pkey')
    )

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, primary_key=True)
    amount_to_be_withdrawn_or_added: Mapped[decimal.Decimal] = mapped_column('amount to be withdrawn or added', Numeric(1000, 1000), nullable=False)
    balance_after_transaction: Mapped[decimal.Decimal] = mapped_column('balance after_transaction', Numeric(1000, 1000), nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    updated_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    account: Mapped['SavingsAccount'] = relationship('SavingsAccount', back_populates='transactions')