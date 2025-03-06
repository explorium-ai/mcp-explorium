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


class ProspectEventType(str, Enum):
    """
    Valid event types for the Explorium Prospects Events API.

    JOB_TITLE_CHANGE: Individual transitioned to a new job title within their current company
    - previous_job_title: str - Employee's previous job title
    - event_time: datetime - Employee left previous role timestamp
    - current_job_title: str - Employee's current job title
    - current_company_name: str - Employee's current workplace
    - current_company_id: str - Current workplace entity ID
    - event_id: str - Job change event ID

    COMPANY_CHANGE: Individual transitioned to a new company
    - previous_company_name: str - Employee's previous workplace name
    - previous_company_id: str - Previous workplace entity ID
    - previous_job_title: str - Employee's previous job title
    - event_time: datetime - Employee left previous company timestamp
    - current_company_name: str - Employee's current workplace name
    - current_company_id: str - Current workplace entity ID
    - current_job_title: str - Employee's current job title
    - event_id: str - Company change event ID

    WORKPLACE_ANNIVERSARY: Individual reached an annual milestone at their current company.
    - full_name: str - Employee's full name
    - event_id: str - Employee event ID
    - company_name: str - Workplace company name
    - years_at_company: int - Number of years at company
    - job_title: str - Employee's job title
    - job_anniversary_date: datetime - Employee event timestamp
    - event_time: datetime - Workplace anniversary date
    - linkedin_url: str - Employee LinkedIn URL
    """

    JOB_TITLE_CHANGE = "prospect_changed_role"
    COMPANY_CHANGE = "prospect_changed_company"
    WORKPLACE_ANNIVERSARY = "prospect_job_start_anniversary"
