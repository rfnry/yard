from __future__ import annotations

import hashlib

IDENTITIES = {
    "ID-9876": {
        "person_id": "ID-9876",
        "full_name": "Theodore Aksel Branham",
        "date_of_birth": "1978-03-14",
        "address": "412 Wexford Lane, Apt 6B, Portland OR 97201",
        "ssn_last4": "4421",
        "issued_id_type": "drivers_license",
        "issued_id_state": "OR",
    },
    "ID-1024": {
        "person_id": "ID-1024",
        "full_name": "Mariella Souza Carter",
        "date_of_birth": "1985-11-02",
        "address": "8 Oakridge Court, Cambridge MA 02139",
        "ssn_last4": "9087",
        "issued_id_type": "passport",
        "issued_id_state": "MA",
    },
    "ID-5577": {
        "person_id": "ID-5577",
        "full_name": "Devon Hsiao",
        "date_of_birth": "1992-07-21",
        "address": "1903 Larkspur Way, Austin TX 78745",
        "ssn_last4": "3318",
        "issued_id_type": "drivers_license",
        "issued_id_state": "TX",
    },
}

CRIMINAL_RECORDS = {
    "ID-9876": [
        {
            "case_number": "OR-2014-CRM-04412",
            "offense": "Driving Under the Influence (DUI)",
            "disposition": "convicted",
            "sentence": "12 months probation, fine $1,800",
            "date": "2014-08-09",
        }
    ],
    "ID-1024": [],
    "ID-5577": [
        {
            "case_number": "TX-2019-MIS-22041",
            "offense": "Disorderly Conduct",
            "disposition": "dismissed",
            "sentence": None,
            "date": "2019-04-15",
        }
    ],
}

COURT_RECORDS = {
    "OR-2014-CRM-04412": {
        "case_number": "OR-2014-CRM-04412",
        "court": "Multnomah County Circuit Court",
        "case_type": "criminal_misdemeanor",
        "filed_at": "2014-06-12",
        "closed_at": "2014-08-09",
        "parties": ["State of Oregon", "Theodore Aksel Branham"],
        "outcome": "guilty plea entered",
    },
    "MA-2024-CIV-99012": {
        "case_number": "MA-2024-CIV-99012",
        "court": "Middlesex Superior Court",
        "case_type": "civil_contract",
        "filed_at": "2024-02-19",
        "closed_at": None,
        "parties": ["Northbridge Holdings LLC", "Mariella Souza Carter"],
        "outcome": "pending",
    },
}

PROPERTY_RECORDS = {
    "ID-9876": [
        {
            "address": "412 Wexford Lane, Apt 6B, Portland OR 97201",
            "ownership": "tenant",
            "since": "2019-05-01",
            "tax_assessed_value_usd": None,
        }
    ],
    "ID-1024": [
        {
            "address": "8 Oakridge Court, Cambridge MA 02139",
            "ownership": "owner_occupied",
            "since": "2017-09-22",
            "tax_assessed_value_usd": 921_400,
        },
        {
            "address": "12 Sea Cliff Rd, Marblehead MA 01945",
            "ownership": "investment",
            "since": "2022-03-10",
            "tax_assessed_value_usd": 1_180_000,
        },
    ],
    "ID-5577": [],
}

BUSINESS_REGISTRY = {
    "BIZ-NHB-01": {
        "business_id": "BIZ-NHB-01",
        "legal_name": "Northbridge Holdings LLC",
        "state_of_formation": "DE",
        "registered_agent": "Corporation Trust Center",
        "principals": ["Mariella Souza Carter"],
        "active": True,
    },
}

EMPLOYMENT_HISTORY = {
    "ID-9876": [
        {"employer": "Pacific Logistics Co.", "role": "warehouse supervisor", "from": "2017-04", "to": None},
    ],
    "ID-1024": [
        {"employer": "Northbridge Holdings LLC", "role": "managing partner", "from": "2017-08", "to": None},
        {"employer": "Caldwell Capital", "role": "associate", "from": "2010-06", "to": "2017-07"},
    ],
    "ID-5577": [
        {"employer": "Lumen Pictures Studio", "role": "post-production engineer", "from": "2020-01", "to": None},
    ],
}


def _digest(value: str) -> int:
    return int(hashlib.sha256(value.encode()).hexdigest(), 16)


def fallback_identity(person_id: str) -> dict[str, object]:
    digest = _digest(person_id)
    return {
        "person_id": person_id,
        "full_name": f"Synthesized Person {person_id[-4:]}",
        "date_of_birth": "1980-01-01",
        "address": "(no record on file)",
        "ssn_last4": str(digest % 10_000).zfill(4),
        "issued_id_type": "unknown",
        "issued_id_state": "ZZ",
        "_synthesized": True,
    }
