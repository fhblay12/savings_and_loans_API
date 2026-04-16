import pytest
from unittest.mock import MagicMock
from repositories.transaction_repo import (
    create_transaction,
    get_transaction,
    delete_transaction,
    update_transaction,
)


# ---------------------------------------------------------------------
# TEST SETUP
# ---------------------------------------------------------------------
class TestTransactionRepo:

    def setup_method(self):
        self.db = MagicMock()

        self.account_id = "acc-1"
        self.transaction_id = "tx-1"

    # =========================================================
    # CREATE TRANSACTION
    # =========================================================
    def test_create_transaction_success(self):
        # mock account exists
        self.db.query.return_value.filter.return_value.first.return_value = MagicMock()

        result = create_transaction(
            account_id=self.account_id,
            amount=100.0,
            tx_type="deposit",
            db=self.db
        )

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.account_id == self.account_id
        assert result.amount_to_be_withdrawn_or_added == 100.0

    def test_create_transaction_account_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            create_transaction(
                account_id=self.account_id,
                amount=100.0,
                tx_type="deposit",
                db=self.db
            )

    # =========================================================
    # GET TRANSACTION
    # =========================================================
    def test_get_transaction_success(self):
        mock_tx = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_tx

        result = get_transaction(self.db, self.transaction_id)

        assert result == mock_tx

    def test_get_transaction_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            get_transaction(self.db, self.transaction_id)

    # =========================================================
    # DELETE TRANSACTION
    # =========================================================
    def test_delete_transaction_success(self):
        mock_tx = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_tx

        result = delete_transaction(self.db, self.transaction_id)

        self.db.delete.assert_called_once_with(mock_tx)
        self.db.commit.assert_called_once()

        assert result == mock_tx

    def test_delete_transaction_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            delete_transaction(self.db, self.transaction_id)

    # =========================================================
    # UPDATE TRANSACTION
    # =========================================================
    def test_update_transaction_success(self):
        mock_tx = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_tx

        result = update_transaction(
            db=self.db,
            transaction_id=self.transaction_id,
            amount=250.0,
            tx_type="withdrawal"
        )

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert mock_tx.amount_to_be_withdrawn_or_added == 250.0
        assert mock_tx.transaction_type == "withdrawal"

    def test_update_transaction_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_transaction(
                db=self.db,
                transaction_id=self.transaction_id,
                amount=100.0,
                tx_type="deposit"
            )
if __name__ == "__main__":
    pytest.main()