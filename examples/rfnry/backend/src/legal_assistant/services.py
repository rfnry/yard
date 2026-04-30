from __future__ import annotations

from src.legal_assistant.data import (
    BUSINESS_REGISTRY,
    COURT_RECORDS,
    CRIMINAL_RECORDS,
    EMPLOYMENT_HISTORY,
    IDENTITIES,
    PROPERTY_RECORDS,
    fallback_identity,
)


def get_identity(person_id: str) -> dict[str, object]:
    person_id_upper = person_id.upper()
    record = IDENTITIES.get(person_id_upper)
    if record is not None:
        return record
    return fallback_identity(person_id_upper)


def get_criminal_records(person_id: str) -> list[dict[str, object]]:
    return CRIMINAL_RECORDS.get(person_id.upper(), [])


def get_court_record(case_number: str) -> dict[str, object] | None:
    return COURT_RECORDS.get(case_number.upper())


def get_property_records(person_id: str) -> list[dict[str, object]]:
    return PROPERTY_RECORDS.get(person_id.upper(), [])


def get_business(business_id: str) -> dict[str, object] | None:
    return BUSINESS_REGISTRY.get(business_id.upper())


def get_employment_history(person_id: str) -> list[dict[str, object]]:
    return EMPLOYMENT_HISTORY.get(person_id.upper(), [])
