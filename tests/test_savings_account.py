import pytest
from unittest.mock import MagicMock

from repositories.savings_account_repo import (
    create_savings_account_repo,
    get_savings_accounts,
    delete_savings_account,
    get_savings_account_by_id,
    update_savings_account,
)


class BadAccountData:
    balance = 1000
    admin_id = "admin-1"
    is_verified = False
    # missing customer_id on purpose
# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_account_create():
    mock = MagicMock()
    mock.customer_id = "cust-1"
    mock.balance = 1000
    mock.admin_id = "admin-1"
    mock.is_verified = False
    return mock


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestSavingsAccountRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.account_data = _make_account_create()

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================
    def test_create_account_success(self):
        #Arrange(Setup inputs) & Act(Call the function)
        result = create_savings_account_repo(self.db, self.account_data)

       #Assert(Verify outputs)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.customer_id == "cust-1"
        assert result.balance == 1000

    def test_create_account_exception(self):
        bad_data = BadAccountData()

        with pytest.raises(ValueError) as exc_info:
            create_savings_account_repo(self.db, bad_data)
        assert "Error creating savings account for customer" in str(exc_info.value)
    # =========================================================
    # GET ACCOUNTS BY CUSTOMER
    # =========================================================
    def test_get_accounts_success(self):
        self.db.query.return_value.filter.return_value.all.return_value = ["acc1", "acc2"]

        result = get_savings_accounts(self.db, "cust-1")

        assert len(result) == 2

    def test_get_accounts_not_found(self):
        self.db.query.return_value.filter.return_value.all.return_value = []

        with pytest.raises(ValueError):
            get_savings_accounts(self.db, "cust-1")

    # =========================================================
    # GET BY ID
    # =========================================================
    def test_get_account_by_id_success(self):
        mock_account = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_account

        result = get_savings_account_by_id(self.db, "acc-1")

        assert result == mock_account

    def test_get_account_by_id_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            get_savings_account_by_id(self.db, "acc-1")

    # =========================================================
    # DELETE ACCOUNT
    # =========================================================
    def test_delete_account_success(self):
        mock_account = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_account

        result = delete_savings_account(self.db, "acc-1")

        self.db.delete.assert_called_once_with(mock_account)
        self.db.commit.assert_called_once()

        assert result == mock_account

    def test_delete_account_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            delete_savings_account(self.db, "acc-1")

    # =========================================================
    # UPDATE ACCOUNT
    # =========================================================
    def test_update_account_success(self):
        mock_account = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_account

        update_data = MagicMock()
        update_data.dict.return_value = {
            "balance": 5000,
            "is_verified": True
        }

        result = update_savings_account(self.db, "acc-1", update_data)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert mock_account.balance == 5000
        assert mock_account.is_verified is True

    def test_update_account_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_savings_account(self.db, "acc-1", MagicMock())

if __name__ == "__main__":
    pytest.main()