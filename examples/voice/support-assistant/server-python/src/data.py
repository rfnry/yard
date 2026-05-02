from __future__ import annotations

from dataclasses import dataclass


class UnknownRental(Exception):
    pass


class UnknownAccount(Exception):
    pass


@dataclass
class Account:
    id: str
    name: str
    email: str


@dataclass
class Rental:
    id: str
    account_id: str
    vehicle: str
    pickup_date: str
    return_date: str
    status: str
    daily_rate_usd: float


_ACCOUNTS: dict[str, Account] = {}
_RENTALS: dict[str, Rental] = {}


def seed() -> None:
    _ACCOUNTS.clear()
    _RENTALS.clear()
    _ACCOUNTS["A-001"] = Account(id="A-001", name="Alex Chen", email="alex@example.com")
    _ACCOUNTS["A-002"] = Account(id="A-002", name="Bea Park", email="bea@example.com")
    _RENTALS["R-1001"] = Rental(
        id="R-1001",
        account_id="A-001",
        vehicle="Toyota Corolla 2024",
        pickup_date="2026-04-20",
        return_date="2026-04-23",
        status="completed",
        daily_rate_usd=42.0,
    )
    _RENTALS["R-1002"] = Rental(
        id="R-1002",
        account_id="A-001",
        vehicle="Tesla Model 3 2025",
        pickup_date="2026-05-10",
        return_date="2026-05-15",
        status="active",
        daily_rate_usd=95.0,
    )
    _RENTALS["R-1003"] = Rental(
        id="R-1003",
        account_id="A-002",
        vehicle="Ford Bronco 2024",
        pickup_date="2026-05-01",
        return_date="2026-05-04",
        status="completed",
        daily_rate_usd=120.0,
    )


def get_rental(rental_id: str) -> Rental:
    if rental_id not in _RENTALS:
        raise UnknownRental(f"no rental with id {rental_id!r}")
    return _RENTALS[rental_id]


def get_account(account_id: str) -> Account:
    if account_id not in _ACCOUNTS:
        raise UnknownAccount(f"no account with id {account_id!r}")
    return _ACCOUNTS[account_id]


def list_rentals_for_account(account_id: str) -> list[Rental]:
    return [r for r in _RENTALS.values() if r.account_id == account_id]


def refund_rental(rental_id: str, *, reason: str) -> Rental:
    rental = get_rental(rental_id)
    rental.status = "refunded"
    return rental


seed()
