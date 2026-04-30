from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.legal_assistant import services

router = APIRouter(tags=["legal-assistant"])


@router.get("/identity/{person_id}")
async def get_identity(person_id: str) -> dict[str, object]:
    return services.get_identity(person_id)


@router.get("/criminal-records/{person_id}")
async def get_criminal_records(person_id: str) -> dict[str, object]:
    return {"person_id": person_id.upper(), "records": services.get_criminal_records(person_id)}


@router.get("/court-records/{case_number}")
async def get_court_record(case_number: str) -> dict[str, object]:
    record = services.get_court_record(case_number)
    if record is None:
        raise HTTPException(status_code=404, detail=f"case not found: {case_number}")
    return record


@router.get("/property-records/{person_id}")
async def get_property_records(person_id: str) -> dict[str, object]:
    return {"person_id": person_id.upper(), "properties": services.get_property_records(person_id)}


@router.get("/business-registry/{business_id}")
async def get_business(business_id: str) -> dict[str, object]:
    record = services.get_business(business_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"business not found: {business_id}")
    return record


@router.get("/employment-history/{person_id}")
async def get_employment_history(person_id: str) -> dict[str, object]:
    return {"person_id": person_id.upper(), "history": services.get_employment_history(person_id)}
