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
        result = delete_admin(self.db, "fake-id")
        assert result is None

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

    def test_verify_loan_not_found(self):
        self.db.query.return_value.filter.return_value.all.return_value = []

        with pytest.raises(ValueError):
            verify_loan(self.db, ["loan1"])

if __name__ == "__main__":    pytest.main()