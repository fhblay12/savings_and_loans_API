import pytest
from unittest.mock import MagicMock, patch

from repositories.employment_details_repo import (
    create_employment_details,
    update_employment_detail,
    delete_employment_detail,
    get_member_by_id,
)


# ---------------------------------------------------------------------
# TEST DATA FACTORY
# ---------------------------------------------------------------------
def _make_employment_create(overrides=None):
    base = MagicMock()
    base.employer_first_name = "John"
    base.employer_last_name = "Doe"
    base.customer_id = "cust-1"
    base.job_title = "Engineer"
    base.monthly_income = 5000
    base.employment_type = "Full-time"
    base.employment_start_date = "2024-01-01"

    if overrides:
        for k, v in overrides.items():
            setattr(base, k, v)

    return base
from types import SimpleNamespace

def _make_employment_create_invalid():
    return SimpleNamespace(
        employer_last_name="Doe",
        customer_id="cust-1",
        job_title="Engineer",
        monthly_income=5000,
        employment_type="Full-time",
        employment_start_date="2024-01-01"
        # ❌ employer_first_name missing → real AttributeError
    )


# ---------------------------------------------------------------------
# TEST CLASS
# ---------------------------------------------------------------------
class TestEmploymentRepo:

    def setup_method(self):
        self.db = MagicMock()
        self.employment_data = _make_employment_create()

    # =========================================================
    # CREATE
    # =========================================================
    def test_create_employment_success(self):
        result = create_employment_details(self.db, self.employment_data)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert result.employer_first_name == "John"

   

    def test_create_employment_failure(self):
        invalid_data = _make_employment_create_invalid()


        with pytest.raises(ValueError):
            create_employment_details(self.db, invalid_data)

    # =========================================================
    # UPDATE
    # =========================================================
    def test_update_employment_success(self):
        mock_employment = MagicMock()

        self.db.query.return_value.filter.return_value.first.return_value = mock_employment

        update_data = MagicMock()
        update_data.employer_first_name = "Jane"
        update_data.employer_last_name = "Smith"
        update_data.job_title = "Manager"
        update_data.monthly_income = 7000
        update_data.employment_type = "Part-time"

        result = update_employment_detail(self.db, "emp-1", update_data)

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        assert mock_employment.employer_first_name == "Jane"

    def test_update_employment_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            update_employment_detail(self.db, "emp-1", MagicMock())

    # =========================================================
    # DELETE
    # =========================================================
    def test_delete_employment_success(self):
        mock_employment = MagicMock()

        self.db.query.return_value.filter.return_value.first.return_value = mock_employment

        result = delete_employment_detail(self.db, "emp-1")

        self.db.delete.assert_called_once_with(mock_employment)
        self.db.commit.assert_called_once()

        assert result == mock_employment

    def test_delete_employment_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            delete_employment_detail(self.db, "emp-1")

    # =========================================================
    # GET BY ID
    # =========================================================
    def test_get_member_by_id_success(self):
        mock_employment = MagicMock()
        self.db.query.return_value.filter.return_value.first.return_value = mock_employment

        result = get_member_by_id(self.db, "emp-1")

        assert result == mock_employment

    def test_get_member_by_id_not_found(self):
        self.db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(ValueError):
            get_member_by_id(self.db, "emp-1")

if __name__ == "__main__":
    pytest.main()