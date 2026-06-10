import pytest
from unittest.mock import MagicMock, patch

from repositories.admin_repo import (
    create_admin,
    login_admin,
    update_admin,
    delete_admin,
    verify_account,
    verify_loan,
    get_admin_savings_accounts,
    get_admin_loans,
    get_admin_unverified_loan,
    get_admin_unverified_savings_accounts,
    random_account_administrator
)

from schemas.admin_schema import AdminCreate, AdminUpdate, LoginRequest


# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_admin_create(overrides=None):
    base = {
        "admin_role": "Account Administrator",
        "admin_first_name": "John",
        "admin_last_name": "Doe",
        "email": "admin@example.com",
        "password": "plain_password",
    }

    if overrides:
        base.update(overrides)

    return AdminCreate(**base)


def _make_login():
    return LoginRequest(
        email="admin@example.com",
        password="plain_password"
    )


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestAdminRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.admin_data = _make_admin_create()
        self.login_data = _make_login()

    # =========================================================
    # CREATE ADMIN
    # =========================================================
    @patch("repositories.admin_repo.hash_password")
    def test_create_admin_success(self, mock_hash):
        mock_hash.return_value = "hashed_pw"

        # no existing admin
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = create_admin(self.db, self.admin_data)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.email == self.admin_data.email

    @patch("repositories.admin_repo.hash_password")
    def test_create_admin_duplicate(self, mock_hash):
        mock_hash.return_value = "hashed_pw"

        self.db.query.return_value.filter.return_value.first.return_value = MagicMock()

        with pytest.raises(ValueError):
            create_admin(self.db, self.admin_data)

    
    
    #`=========================================================
    # GET RANDOM ADMIN
    # =========================================================
    def test_random_admin_selection(self):
        # Mock multiple admins
        mock_admin1 = MagicMock()
        mock_admin1.email = "admin1@example.com"
        mock_admin1.admin_role = "Account Administrator"
        mock_admin2 = MagicMock()
        mock_admin2.email = "admin2@example.com"
        mock_admin2.admin_role = "Account Administrator"
        self.db.query.return_value.filter.return_value.all.return_value = [mock_admin1, mock_admin2]

        result = random_account_administrator(self.db)

        assert result in [mock_admin1, mock_admin2]
    # =========================================================
    # LOGIN ADMIN
    # =========================================================
    @patch("repositories.admin_repo.verify_password")
    def test_login_success(self, mock_verify):
        mock_verify.return_value = True

        mock_admin = MagicMock()
        mock_admin.email = self.login_data.email
        mock_admin.password = "hashed_pw"

        self.db.query.return_value.filter.return_value.first.return_value = mock_admin

        result = login_admin(self.db, self.login_data)

        assert result.email == self.login_data.email

    @patch("repositories.admin_repo.verify_password")
    def test_login_wrong_password(self, mock_verify):
        mock_verify.return_value = False

        mock_admin = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_admin

        with pytest.raises(ValueError):
            login_admin(self.db, self.login_data)

    def test_login_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            login_admin(self.db, self.login_data)

    # =========================================================
    # UPDATE ADMIN
    # =========================================================
    @patch("repositories.admin_repo.hash_password")
    def test_update_admin_success(self, mock_hash):
        mock_hash.return_value = "new_hash"

        mock_admin = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_admin

        update_data = MagicMock()
        update_data.dict.return_value = {"password": "new_pass"}

        result = update_admin(self.db, "fake-id", update_data)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result is not None

    def test_update_admin_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_admin(self.db, "fake-id", MagicMock())

    # =========================================================
    # DELETE ADMIN
    # =========================================================
    def test_delete_admin_success(self):
        mock_admin = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_admin

        result = delete_admin(self.db, "fake-id")

        self.db.delete.assert_called_once_with(mock_admin)
        self.db.commit.assert_called_once()

    def test_delete_admin_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        # your version returns None instead of raising
        with pytest.raises(ValueError):
            delete_admin(self.db, "fake-id")

    # =========================================================
    # VERIFY ACCOUNT
    # =========================================================
    def test_verify_account(self):
        mock_account = MagicMock()
        mock_account.account_id = "123"

        self.db.query.return_value.filter.return_value.all.return_value = [mock_account]

        result = verify_account(self.db, ["123"])

        self.db.commit.assert_called_once()
        assert result[0].is_verified is True

    def test_verify_account_not_found(self):
        self.db.query.return_value.filter.return_value.all.return_value = []

        with pytest.raises(ValueError):
            verify_account(self.db, ["123"])

    def test_get_admin_savings_accounts_success(self):
            # Mock customer
            mock_customer = MagicMock()
            mock_customer.first_name = "John"
            mock_customer.last_name = "Doe"

            # Mock account
            mock_account = MagicMock()
            mock_account.customer_id = "customer-id"
            mock_account.customer = mock_customer
            mock_account.balance = 500.0
            mock_account.created_date = "2026-01-01"
            mock_account.admin_id = "admin-id"
            mock_account.is_verified = True

            # Mock query chain
            self.db.query.return_value.join.return_value.filter.return_value.all.return_value = [
                mock_account
            ]

            result = get_admin_savings_accounts(self.db, "admin-id")

            assert len(result) == 1
            assert result[0]["owner_first_name"] == "John"
            assert result[0]["owner_last_name"] == "Doe"
            assert result[0]["balance"] == 500.0
            assert result[0]["is_verified"] is True
    def test_get_admin_savings_accounts_not_found(self):
        self.db.query.return_value.join.return_value.filter.return_value.all.return_value = []
        with pytest.raises(ValueError):
            get_admin_savings_accounts(self.db, "admin-id")

    def test_get_admin_unverified_savings_accounts(self):
    # Mock customer
        mock_customer = MagicMock()
        mock_customer.first_name = "John"
        mock_customer.last_name = "Doe"

        # Mock account
        mock_account = MagicMock()
        mock_account.customer_id = "customer-id"
        mock_account.customer = mock_customer
        mock_account.balance = 500.0
        mock_account.created_date = "2026-01-01"
        mock_account.admin_id = "admin-id"
        mock_account.is_verified = False

        # Mock query chain
        self.db.query.return_value.join.return_value.filter.return_value.filter.return_value.all.return_value = [
            mock_account
        ]

        result = get_admin_unverified_savings_accounts(self.db, "admin-id")

        assert len(result) == 1
        assert result[0]["owner_first_name"] == "John"
        assert result[0]["owner_last_name"] == "Doe"
        assert result[0]["balance"] == 500.0
        assert result[0]["is_verified"] is False   # ✅ FIX
    # =========================================================
    # VERIFY LOAN
    # =========================================================
    def test_verify_loan(self):
        mock_loan = MagicMock()
        mock_loan.loan_id = "loan1"

        self.db.query.return_value.filter.return_value.all.return_value = [mock_loan]

        result = verify_loan(self.db, ["loan1"])

        self.db.commit.assert_called_once()
        assert result[0].is_verified is True

    def test_get_admin_loans_success(self):
        # Mock customer
        mock_customer = MagicMock()
        mock_customer.first_name = "John"
        mock_customer.last_name = "Doe"

        # Mock loan
        mock_loan = MagicMock()
        mock_loan.customer_id = "customer-id"
        mock_loan.customer = mock_customer
        mock_loan.loan_amount = 1000.0
        mock_loan.created_date = "2026-01-01"
        mock_loan.time_of_closure = None
        mock_loan.is_verified = True
        mock_loan.loan_status = "approved"   # ✅ REQUIRED (your function uses this)

        # ✅ FIX: correct chain
        self.db.query.return_value.options.return_value.filter.return_value.all.return_value = [
            mock_loan
        ]

        result = get_admin_loans(self.db, "admin-id")

        assert len(result) == 1
        assert result[0]["owner_first_name"] == "John"
        assert result[0]["loan_status"] == "approved"

    def test_get_admin_loans_not_found(self):
        # ✅ Correct chain
        self.db.query.return_value.options.return_value.filter.return_value.all.return_value = []

        with pytest.raises(ValueError):
            get_admin_loans(self.db, "admin-id")

    def test_verify_loan_not_found(self):
        self.db.query.return_value.filter.return_value.all.return_value = []

        with pytest.raises(ValueError):
            verify_loan(self.db, ["loan1"])

    def test_get_admin_unverified_loan_success(self):
        # Mock customer
        mock_customer = MagicMock()
        mock_customer.first_name = "Jane"
        mock_customer.last_name = "Doe"

        # Mock loan
        mock_loan = MagicMock()
        mock_loan.customer_id = "customer-id"
        mock_loan.customer = mock_customer  # ✅ IMPORTANT (same issue as before)
        mock_loan.loan_amount = 1000.0
        mock_loan.created_date = "2026-01-01"
        mock_loan.is_verified = False
        mock_loan.admin_id = "admin-id"

        # Mock query chain
        self.db.query.return_value.join.return_value.filter.return_value.filter.return_value.all.return_value = [
            mock_loan
        ]

        result = get_admin_unverified_loan(self.db, "admin-id")

        assert len(result) == 1
        assert result[0]["owner_first_name"] == "Jane"
        assert result[0]["owner_last_name"] == "Doe"
        assert result[0]["loan_amount"] == 1000.0
        assert result[0]["is_verified"] is False   # ✅ FIX

if __name__ == "__main__":    pytest.main()