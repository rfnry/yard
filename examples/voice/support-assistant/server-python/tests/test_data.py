from __future__ import annotations

import pytest

from src.data import (
    UnknownAccount,
    UnknownRental,
    get_account,
    get_rental,
    list_rentals_for_account,
    refund_rental,
    seed,
)


def test_seed_populates_known_records() -> None:
    seed()
    rental = get_rental("R-1001")
    assert rental.account_id == "A-001"


def test_get_rental_unknown_id_raises() -> None:
    seed()
    with pytest.raises(UnknownRental):
        get_rental("R-9999")


def test_get_account_unknown_id_raises() -> None:
    seed()
    with pytest.raises(UnknownAccount):
        get_account("A-9999")


def test_list_rentals_for_account_returns_only_owned_rentals() -> None:
    seed()
    rentals = list_rentals_for_account("A-001")
    assert all(r.account_id == "A-001" for r in rentals)
    assert len(rentals) >= 1


def test_refund_rental_marks_status_and_is_idempotent() -> None:
    seed()
    rental = refund_rental("R-1001", reason="customer requested")
    assert rental.status == "refunded"
    again = refund_rental("R-1001", reason="customer requested")
    assert again.status == "refunded"
