from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from .shared import BasePaginatedResponse, RangeInt
from .enum_types import JobLevel, JobDepartment, NumberOfEmployeesRange


class Prospect(BaseModel):
    prospect_id: str
    full_name: Optional[str] = Field(default=None)
    country_name: Optional[str] = Field(default=None)
    region_name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    linkedin: Optional[str] = Field(default=None)
    experience: Optional[str] = Field(default=None)
    skills: Optional[str] = Field(default=None)
    interests: Optional[str] = Field(default=None)
    company_name: Optional[str] = Field(default=None)
    company_website: Optional[str] = Field(default=None)
    company_linkedin: Optional[str] = Field(default=None)
    job_department: Optional[str] = Field(default=None)
    job_seniority_level: Optional[List[str]] = Field(default=None)
    job_title: Optional[str] = Field(default=None)


class FetchProspectsFilters(BaseModel):
    """
    Prospect search filters.

    These filters enable precise targeting of potential contacts by refining search criteria based on attributes
    such as email and phone availability, job roles, professional experience, and company-related details.
    When using these filters, it is advisable to call an autocomplete tool to obtain the latest list of supported values
    for industry categories (google_category, naics_category, linkedin_category) before initiating a search.
    Only one industry category filter should be provided at a time to avoid conflicts.
    """

    has_email: Optional[bool] = Field(
        default=None,
        description="Filter prospects to include only those with a verified email address.",
        examples=[True]
    )
    has_phone_number: Optional[bool] = Field(
        default=None,
        description="Filter prospects to include only those with an available phone number.",
        examples=[True]
    )

    job_level: Optional[list[JobLevel]] = Field(
        default=None,
        description="Filter prospects based on their job seniority level (e.g., 'vp', 'director').",
        examples=[["vp", "director"]]
    )
    job_department: Optional[list[JobDepartment]] = Field(
        default=None,
        description="Filter prospects based on their department (e.g., 'Engineering', 'Marketing').",
        examples=[["Engineering", "Marketing"]]
    )
    business_id: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by specifying one or more business IDs as registered in the system. "
                    "Pass multiple IDs in a list to filter prospects that match any of the provided IDs.",
        examples=[["8adce3ca1cef0c986b22310e369a0793", "010146d2ec90d2e94b9dd85eced59d76"]]
    )
    job_title: Optional[list[str]] = Field(
        default=None,
        description="Free text filter for prospect job titles (e.g., 'Software Engineer', 'Data Scientist').",
        examples=[["Software Engineer", "Data Scientist"]]
    )

    country_code: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects based on a 2-letter ISO Alpha-2 country code representing the prospect's location (e.g., 'US', 'CA').",
        examples=[["US", "CA"]]
    )
    region_country_code: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects based on a region code that combines a region identifier with the country's code (e.g., 'US-NY', 'IL-TA').",
        examples=[["US-NY", "IL-TA"]]
    )
    company_country_code: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by the 2-letter ISO Alpha-2 country code where their company is primarily located.",
        examples=[["US"]]
    )
    company_region_country_code: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by the region code (combining region and country) where their company is headquartered (e.g., 'US-CA').",
        examples=[["US-CA"]]
    )
    city_region_country: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects using a combined city, region, and country string (e.g., 'Miami, FL, US', 'Tel Aviv, IL').",
        examples=[["Miami, FL, US", "Tel Aviv, IL"]]
    )
    company_name: Optional[list[str]] = Field(
        default=None,
        description="Free text filter for the prospect's company name (e.g., 'Google', 'Microsoft').",
        examples=[["Google", "Microsoft"]]
    )

    company_size: Optional[list[NumberOfEmployeesRange]] = Field(
        default=None,
        description="Filter prospects by the employee count range of their company (e.g., '11-50', '51-200').",
        examples=[["11-50", "51-200"]]
    )
    company_revenue: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by the revenue range of their company (e.g., '0-500K', '1M-5M').",
        examples=[["0-500K", "1M-5M"]]
    )

    total_experience_months: Optional[RangeInt] = Field(
        default=None,
        description="Filter prospects by their total work experience in months (e.g., between 12 and 120 months).",
        examples=[{"gte": 12, "lte": 120}]
    )
    current_role_months: Optional[RangeInt] = Field(
        default=None,
        description="Filter prospects based on the number of months they have held their current role (e.g., between 6 and 24 months).",
        examples=[{"gte": 6, "lte": 24}]
    )

    google_category: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by their company's Google industry category (e.g., 'construction').",
        examples=[["construction"]]
    )
    naics_category: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by their company's NAICS classification code (e.g., '541512' for software services).",
        examples=[["541512"]]
    )
    linkedin_category: Optional[list[str]] = Field(
        default=None,
        description="Filter prospects by their company's LinkedIn industry category (e.g., 'retail').",
        examples=[["retail"]]
    )


class FetchProspectsResponse(BasePaginatedResponse):
    data: list[Prospect]


class ProspectMatchInput(BaseModel):
    """
    Identifiers for matching a prospect.
    Use full_name and company_name together for an accurate match. Additional identifiers such as email,
    phone number, LinkedIn URL, or business ID can also be provided to enhance matching precision.
    """

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
