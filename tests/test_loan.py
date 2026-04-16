import pytest
from unittest.mock import MagicMock

from repositories.loan_repo import (
    create_loan_details,
    update_loan_details,
    get_loans,
    get_loan_by_id,
    delete_loan,
    create_collateral,
)


# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_loan_create():
    mock_loan = MagicMock()
    mock_loan.dict.return_value = {
        "loan_amount": 5000,
        "interest_rate": 10,
        "term_in_months": 12
    }
    return mock_loan


def _make_admin():
    admin = MagicMock()
    admin.admin_id = "admin-1"
    return admin


def _make_update():
    update = MagicMock()
    update.dict.return_value = {
        "loan_amount": 7000
    }
    return update


def _make_collateral():
    collateral = MagicMock()
    collateral.collateral_type = "Car"
    collateral.collateral_value = 10000
    return collateral


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestLoanRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.loan = _make_loan_create()
        self.admin = _make_admin()
        self.update = _make_update()
        self.collateral = _make_collateral()

    # =========================================================
    # CREATE LOAN
    # =========================================================
    def test_create_loan_success(self):
        result = create_loan_details(self.db, self.loan, self.admin, "cust-1")

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.customer_id == "cust-1"
        assert result.admin_id == "admin-1"
        assert result.loan_status == "Pending"
        assert result.is_verified is False

    # =========================================================
    # UPDATE LOAN
    # =========================================================
    def test_update_loan_success(self):
        mock_loan = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_loan

        result = update_loan_details(self.db, "loan-1", self.update)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert mock_loan.loan_amount == 7000

    def test_update_loan_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_loan_details(self.db, "loan-1", self.update)

    # =========================================================
    # GET LOANS
    # =========================================================
    def test_get_loans(self):
        self.db.query.return_value.filter.return_value.all.return_value = ["loan1", "loan2"]

        result = get_loans(self.db, "cust-1")

        assert len(result) == 2

    # =========================================================
    # GET LOAN BY ID
    # =========================================================
    def test_get_loan_by_id(self):
        self.db.query.return_value.filter.return_value.first.return_value = "loan1"

        result = get_loan_by_id(self.db, "loan-1")

        assert result == "loan1"

    # =========================================================
    # DELETE LOAN
    # =========================================================
    def test_delete_loan_success(self):
        mock_loan = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_loan

        result = delete_loan(self.db, "loan-1")

        self.db.delete.assert_called_once_with(mock_loan)
        self.db.commit.assert_called_once()

        assert result == mock_loan

    def test_delete_loan_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            delete_loan(self.db, "loan-1")

    # =========================================================
    # CREATE COLLATERAL
    # =========================================================
    def test_create_collateral(self):
        result = create_collateral(self.db, self.collateral, "loan-1")

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.loan_id == "loan-1"
        assert result.collateral_type == "Car"

if __name__ == "__main__":
    pytest.main()