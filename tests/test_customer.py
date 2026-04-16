import pytest
from unittest.mock import MagicMock, patch
from datetime import date

from repositories.customer_repo import (
    create_customer,
    customer_login,
    update_customer,
    delete_customer,
)

from schemas.customer_schema import CustomerCreate  # adjust if needed


# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_customer_create(overrides: dict | None = None) -> CustomerCreate:
    base = {
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Main Street",
        "social_security_number": "123-45-6789",
        "government_ID": "ID12345",
        "email": "john.doe@example.com",
        "phone_number": "0800000000",
        "DOB": date(1995, 1, 1),
        "credit_score": 700,
        "customer_type": "standard",
        "password": "plain_password",
    }

    if overrides:
        base.update(overrides)

    return CustomerCreate(**base)


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestCustomerRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.customer_data = _make_customer_create()

    # ================================================================
    # CREATE CUSTOMER
    # ================================================================
    @patch("repositories.customer_repo.hash_password")
    def test_create_customer_success(self, mock_hash):
        mock_hash.return_value = "hashed_pw"

        result = create_customer(self.db, self.customer_data)

        # DB interactions
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        # Business logic
        assert result.email == self.customer_data.email
        assert result.first_name == self.customer_data.first_name

    # ================================================================
    # LOGIN CUSTOMER
    # ================================================================
    @patch("repositories.customer_repo.verify_password")
    def test_login_success(self, mock_verify):
        mock_verify.return_value = True

        mock_customer = MagicMock()
        mock_customer.email = self.customer_data.email
        mock_customer.password = "hashed_pw"

        self.db.query.return_value.filter.return_value.first.return_value = mock_customer

        result = customer_login(self.db, self.customer_data)

        assert result.email == self.customer_data.email

    @patch("repositories.customer_repo.verify_password")
    def test_login_wrong_password(self, mock_verify):
        mock_verify.return_value = False

        mock_customer = MagicMock()
        mock_customer.email = self.customer_data.email
        mock_customer.password = "hashed_pw"

        self.db.query.return_value.filter.return_value.first.return_value = mock_customer

        with pytest.raises(ValueError):
            customer_login(self.db, self.customer_data)

    def test_login_user_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            customer_login(self.db, self.customer_data)

    # ================================================================
    # UPDATE CUSTOMER
    # ================================================================
    @patch("repositories.customer_repo.hash_password")
    def test_update_customer_success(self, mock_hash):
        mock_hash.return_value = "new_hashed_pw"

        mock_customer = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_customer

        update_data = MagicMock()
        update_data.dict.return_value = {"password": "new_password"}

        result = update_customer(self.db, "fake-id", update_data)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result is not None

    def test_update_customer_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_customer(self.db, "fake-id", MagicMock())

    # ================================================================
    # DELETE CUSTOMER
    # ================================================================
    def test_delete_customer_success(self):
        mock_customer = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_customer

        result = delete_customer(self.db, "fake-id")

        self.db.delete.assert_called_once_with(mock_customer)
        self.db.commit.assert_called_once()

    def test_delete_customer_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            delete_customer(self.db, "fake-id")

if __name__ == "__main__":
    pytest.main()