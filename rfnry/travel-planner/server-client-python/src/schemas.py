from __future__ import annotations

from pydantic import BaseModel, Field


class FlightOption(BaseModel):
    carrier: str
    flight_numbers: list[str]
    depart_at: str
    return_at: str
    total_price_usd: float
    layovers: list[str] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)


class FlightOptions(BaseModel):
    origin: str
    destination: str
    options: list[FlightOption] = Field(default_factory=list)
    notes: str = ""


class HotelOption(BaseModel):
    name: str
    neighborhood: str
    nightly_usd: float
    total_usd: float
    rating: float
    review_summary: str
    caveats: list[str] = Field(default_factory=list)


class HotelOptions(BaseModel):
    destination: str
    options: list[HotelOption] = Field(default_factory=list)
    notes: str = ""


class Activity(BaseModel):
    name: str
    day: int
    duration_hours: float
    per_person_usd: float
    ticketed: bool
    fits_mood: str


class ActivityList(BaseModel):
    destination: str
    mood: str = "relaxing"
    activities: list[Activity] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)


class DailyForecast(BaseModel):
    day_index: int
    date: str
    high_f: int
    low_f: int
    precip_pct: int
    summary: str
    confidence: str = "high"


class WeatherForecast(BaseModel):
    destination: str
    days: list[DailyForecast] = Field(default_factory=list)
    advisories: list[str] = Field(default_factory=list)


class TripDay(BaseModel):
    day_index: int
    date: str
    activities: list[str] = Field(default_factory=list)
    weather_summary: str = ""


class TripPlan(BaseModel):
    destination: str
    chosen_flight: str
    flight_rationale: str
    chosen_hotel: str
    hotel_rationale: str
    days: list[TripDay] = Field(default_factory=list)
    cost_breakdown: dict[str, float] = Field(default_factory=dict)
    total_usd: float
    caveats: list[str] = Field(default_factory=list)
