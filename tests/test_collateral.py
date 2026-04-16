import pytest
from unittest.mock import MagicMock

from repositories.collateral_repo import (
    create_collateral_details,
    get_collateral_by_id,
    delete_collateral,
    update_collateral,
)


# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_collateral():
    mock = MagicMock()
    mock.collateral_type = "Car"
    mock.collateral_value = 10000
    return mock


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestCollateralRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.collateral_data = _make_collateral()

    # =========================================================
    # CREATE COLLATERAL
    # =========================================================
    def test_create_collateral_success(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        result = create_collateral_details(self.db, self.collateral_data, "loan-1")

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.loan_id == "loan-1"
        assert result.collateral_type == "Car"

    def test_create_collateral_duplicate(self):
        existing = MagicMock()
        existing.collateral_id = "col-1"

        self.db.query.return_value.filter.return_value.first.return_value = existing

        with pytest.raises(ValueError):
            create_collateral_details(self.db, self.collateral_data, "loan-1")

    # =========================================================
    # GET COLLATERAL
    # =========================================================
    def test_get_collateral_success(self):
        mock_collateral = MagicMock()
        mock_collateral.loan_id = "loan-1"

        self.db.query.return_value.filter.return_value.first.return_value = mock_collateral

        result = get_collateral_by_id(self.db, "col-1")

        assert result == mock_collateral

    def test_get_collateral_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(Exception):  # HTTPException
            get_collateral_by_id(self.db, "col-1")

    # =========================================================
    # DELETE COLLATERAL
    # =========================================================
    def test_delete_collateral_success(self):
        mock_collateral = MagicMock()
        mock_collateral.loan_id = "loan-1"

        self.db.query.return_value.filter.return_value.first.return_value = mock_collateral

        result = delete_collateral(self.db, "col-1")

        self.db.delete.assert_called_once_with(mock_collateral)
        self.db.commit.assert_called_once()

        assert result["message"] == "Collateral deleted successfully"

    def test_delete_collateral_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(Exception):  # HTTPException
            delete_collateral(self.db, "col-1")

    # =========================================================
    # UPDATE COLLATERAL
    # =========================================================
    def test_update_collateral_success(self):
        mock_collateral = MagicMock()
        mock_collateral.loan_id = "loan-1"

        self.db.query.return_value.filter.return_value.first.return_value = mock_collateral

        update_data = MagicMock()
        update_data.collateral_type = "House"
        update_data.collateral_value = 50000

        result = update_collateral(self.db, "col-1", update_data)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert mock_collateral.collateral_type == "House"
        assert mock_collateral.collateral_value == 50000

    def test_update_collateral_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(Exception):  # HTTPException
            update_collateral(self.db, "col-1", MagicMock())

if __name__ == "__main__":
    pytest.main()