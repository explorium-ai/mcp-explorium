from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum
from ._shared import BasePaginatedResponse


class JobLevel(str, Enum):
    """All available job levels."""

    DIRECTOR = "director"
    MANAGER = "manager"
    VP = "vp"
    PARTNER = "partner"
    CXO = "cxo"
    NON_MANAGERIAL = "non-managerial"
    SENIOR = "senior"
    ENTRY = "entry"
    TRAINING = "training"
    UNPAID = "unpaid"


class JobDepartment(str, Enum):
    """All available job departments."""

    CUSTOMER_SERVICE = "customer service"
    DESIGN = "design"
    EDUCATION = "education"
    ENGINEERING = "engineering"
    FINANCE = "finance"
    GENERAL = "general"
    HEALTH = "health"
    HUMAN_RESOURCES = "human resources"
    LEGAL = "legal"
    MARKETING = "marketing"
    MEDIA = "media"
    OPERATIONS = "operations"
    PUBLIC_RELATIONS = "public relations"
    REAL_ESTATE = "real estate"
    SALES = "sales"
    TRADES = "trades"
    UNKNOWN = "unknown"


class Prospect(BaseModel):
    prospect_id: str
    full_name: str | None
    country_name: str | None
    region_name: str | None
    city: str | None
    linkedin: str | None
    experience: str | None
    skills: str | None
    interests: str | None
    company_name: str | None
    company_website: str | None
    company_linkedin: str | None
    job_department: str | None
    job_seniority_level: list[str] | None
    job_title: str | None


class FetchProspectsFilters(BaseModel):
    """Prospect search filters."""

    has_email: None | bool = Field(
        default=False, description="Filters for only prospects that have an email."
    )
    has_phone_number: None | bool = Field(
        default=None, description="Filters for only prospects that have a phone number."
    )
    job_level: None | list[JobLevel] = Field(
        default=None, description="Filter for prospects by their job level."
    )
    job_department: None | list[JobDepartment] = Field(
        default=None, description="Filter for prospects by their job department."
    )
    business_id: None | list[str] = Field(
        default=None,
        description="Filters for prospects working at a specific business, by their Explorium Business ID.",
    )


class FetchProspectsResponse(BasePaginatedResponse):
    data: list[Prospect]


class ProspectMatchInput(BaseModel):
    """Prospect match identifiers."""

    email: str | None = Field(default=None, description="The prospect's email address.")
    phone_number: str | None = Field(
        default=None, description="The prospect's phone number."
    )
    full_name: str | None = Field(
        default=None,
        description="The prospect's full name (can only be used together with company_name).",
    )
    company_name: str | None = Field(
        default=None,
        description="The prospect's company name (can only be used together with full_name).",
    )
    linkedin: str | None = Field(default=None, description="Linkedin url.")
    business_id: str | None = Field(
        default=None, description="Filters the prospect to match the given business id."
    )
