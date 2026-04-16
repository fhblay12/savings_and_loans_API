import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal

from repositories.loan_payment_repo import (
    create_loan_payment,
    get_loan_payment,
    get_loan_payments_by_loan,
    delete_loan_payment,
    update_loan_payment,
)


# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_payment():
    mock = MagicMock()
    mock.payment_amount = 1000
    mock.payment_type = "standard"
    return mock


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestLoanPaymentRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.payment_data = _make_payment()

    # =========================================================
    # CREATE PAYMENT
    # =========================================================
    @patch("repositories.loan_payment_repo.standard_loan_payment")
    def test_create_loan_payment_success(self, mock_standard):
        mock_standard.return_value = None

        mock_loan = MagicMock()
        mock_loan.interest_rate = 10

        self.db.query.return_value.filter.return_value.first.return_value = mock_loan

        result = create_loan_payment(self.db, self.payment_data, "loan-1")

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called()

        assert result.payment_amount == Decimal("1000")

    # ---------------------------------------------------------
    def test_create_loan_payment_loan_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(Exception):
            create_loan_payment(self.db, self.payment_data, "loan-1")

    # ---------------------------------------------------------
    def test_create_loan_payment_missing_interest_rate(self):
        mock_loan = MagicMock()
        mock_loan.interest_rate = None

        self.db.query.return_value.filter.return_value.first.return_value = mock_loan

        with pytest.raises(Exception):
            create_loan_payment(self.db, self.payment_data, "loan-1")

    # ---------------------------------------------------------
    @patch("repositories.loan_payment_repo.standard_loan_payment")
    def test_create_loan_payment_invalid_type(self, mock_standard):
        mock_loan = MagicMock()
        mock_loan.interest_rate = 10

        self.db.query.return_value.filter.return_value.first.return_value = mock_loan

        self.payment_data.payment_type = "invalid"

        with pytest.raises(Exception):
            create_loan_payment(self.db, self.payment_data, "loan-1")

    # =========================================================
    # GET PAYMENT BY ID
    # =========================================================
    def test_get_payment_success(self):
        mock_payment = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_payment

        result = get_loan_payment("pay-1", self.db)

        assert result == mock_payment

    def test_get_payment_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(Exception):
            get_loan_payment("pay-1", self.db)

    # =========================================================
    # GET PAYMENTS BY LOAN
    # =========================================================
    def test_get_payments_by_loan_success(self):
        self.db.query.return_value.filter.return_value.all.return_value = ["p1", "p2"]

        result = get_loan_payments_by_loan("loan-1", self.db)

        assert len(result) == 2

    def test_get_payments_by_loan_not_found(self):
        self.db.query.return_value.filter.return_value.all.return_value = []

        with pytest.raises(Exception):
            get_loan_payments_by_loan("loan-1", self.db)

    # =========================================================
    # DELETE PAYMENT
    # =========================================================
    def test_delete_payment_success(self):
        mock_payment = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_payment

        result = delete_loan_payment("pay-1", self.db)

        self.db.delete.assert_called_once_with(mock_payment)
        self.db.commit.assert_called_once()

        assert result is True

    def test_delete_payment_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(Exception):
            delete_loan_payment("pay-1", self.db)

    # =========================================================
    # UPDATE PAYMENT
    # =========================================================
    def test_update_payment_success(self):
        mock_payment = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_payment

        update_data = MagicMock()
        update_data.dict.return_value = {"payment_amount": 2000}

        result = update_loan_payment(self.db, "pay-1", update_data)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert mock_payment.payment_amount == 2000

    def test_update_payment_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_loan_payment(self.db, "pay-1", MagicMock())

if __name__ == "__main__":
    pytest.main()