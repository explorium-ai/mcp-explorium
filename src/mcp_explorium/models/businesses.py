from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum
from ._shared import BasePaginatedResponse


# Fetch Businesses Filters
class CompanySize(str, Enum):
    """All available company size ranges.
    Possible values:"""

    SIZE_1_10 = "1-10"
    """1-10 employees"""
    SIZE_11_50 = "11-50"
    """11-50 employees"""
    SIZE_51_200 = "51-200"
    """51-200 employees"""
    SIZE_201_500 = "201-500"
    """201-500 employees"""
    SIZE_501_1000 = "501-1000"
    """501-1000 employees"""
    SIZE_1001_5000 = "1001-5000"
    """1001-5000 employees"""
    SIZE_5001_10000 = "5001-10000"
    """5001-10000 employees"""
    SIZE_10001_PLUS = "10001+"
    """10001+ employees"""


class CompanyRevenue(str, Enum):
    """All available company revenue ranges"""

    REV_0_1M = "0-1M"
    """$0-1M annual revenue"""
    REV_1M_5M = "1M-5M"
    """$1M-5M annual revenue"""
    REV_5M_10M = "5M-10M"
    """$5M-10M annual revenue"""
    REV_10M_50M = "10M-50M"
    """$10M-50M annual revenue"""
    REV_50M_100M = "50M-100M"
    """$50M-100M annual revenue"""
    REV_100M_500M = "100M-500M"
    """$100M-500M annual revenue"""
    REV_500M_1B = "500M-1B"
    """$500M-1B annual revenue"""
    REV_1B_10B = "1B-10B"
    """$1B-10B annual revenue"""
    REV_10B_100B = "10B-100B"
    """$10B-100B annual revenue"""


class CompanyAge(str, Enum):
    """All available company age ranges"""

    AGE_0_3 = "0-3"
    """0-3 years"""
    AGE_4_10 = "4-10"
    """4-10 years"""
    AGE_11_20 = "11-20"
    """11-20 years"""
    AGE_20_PLUS = "20+"
    """20+ years"""


class FetchBusinessesFilters(BaseModel):
    """Business search filters."""

    country_code: None | list[str] = Field(
        default=None,
        description="A list of lowercase two-letter ISO country codes. Example: ['us', 'ca'] will return businesses from United States and Canada only.",
    )
    region_country_code: None | list[str] = Field(
        default=None,
        description="A list of lowercase region-country codes in the format 'REGION-CC' where CC is the two-letter ISO country code. Example: ['na-us', 'eu-fr'] will return businesses from North America-United States and Europe-France.",
    )
    company_size: None | list[CompanySize] = Field(
        default=None, description="Filters accounts based on the number of employees."
    )
    company_revenue: None | list[CompanyRevenue] = Field(
        default=None, description="Filters accounts based on the annual revenue."
    )
    company_age: None | list[CompanyAge] = Field(
        default=None, description="Filters accounts by the age of the company in years."
    )
    google_category: None | list[str] = Field(
        default=None,
        description='Filters accounts by categories as classified in Google. Example: ["paving contractor", "retail"]',
    )
    naics_category: None | list[str] = Field(
        default=None,
        description='Filters accounts by the North American Industry Classification System categories. Example: ["23", "5611"]',
    )
    linkedin_category: None | list[str] = Field(
        default=None,
        description='Filters accounts by categories as used in LinkedIn. Example: ["software development", "investment banking"]',
    )


class Business(BaseModel):
    business_id: str
    name: str
    domain: str | None
    logo: str | None
    country_name: str
    number_of_employees_range: str
    yearly_revenue_range: str
    website: str | None
    business_description: str | None
    region: str | None
    naics: int | None
    naics_description: str | None
    sic_code: str | None
    sic_code_description: str | None


class FetchBusinessesResponse(BasePaginatedResponse):
    data: list[Business]


class MatchBusinessInput(BaseModel):
    """Input for matching businesses in bulk. Use multiple identifiers for higher match accuracy."""

    name: str | None = None
    domain: str | None = None


class BusinessEventType(str, Enum):
    """Valid event types for the Explorium Business Events API."""

    IPO_ANNOUNCEMENT = "ipo_announcement"
    NEW_FUNDING_ROUND = "new_funding_round"
    NEW_INVESTMENT = "new_investment"
    NEW_PRODUCT = "new_product"
    NEW_OFFICE = "new_office"
    CLOSING_OFFICE = "closing_office"
    NEW_PARTNERSHIP = "new_partnership"

    # Department increases
    INCREASE_ENGINEERING = "increase_in_engineering_department"
    INCREASE_SALES = "increase_in_sales_department"
    INCREASE_MARKETING = "increase_in_marketing_department"
    INCREASE_OPERATIONS = "increase_in_operations_department"
    INCREASE_CUSTOMER_SERVICE = "increase_in_customer_service_department"
    INCREASE_ALL = "increase_in_all_departments"

    # Department decreases
    DECREASE_ENGINEERING = "decrease_in_engineering_department"
    DECREASE_SALES = "decrease_in_sales_department"
    DECREASE_MARKETING = "decrease_in_marketing_department"
    DECREASE_OPERATIONS = "decrease_in_operations_department"
    DECREASE_CUSTOMER_SERVICE = "decrease_in_customer_service_department"
    DECREASE_ALL = "decrease_in_all_departments"

    # Hiring events
    EMPLOYEE_JOINED = "employee_joined_company"
    HIRING_CREATIVE = "hiring_in_creative_department"
    HIRING_EDUCATION = "hiring_in_education_department"
    HIRING_ENGINEERING = "hiring_in_engineering_department"
    HIRING_FINANCE = "hiring_in_finance_department"
    HIRING_HEALTH = "hiring_in_health_department"
    HIRING_HR = "hiring_in_human_resources_department"
    HIRING_LEGAL = "hiring_in_legal_department"
    HIRING_MARKETING = "hiring_in_marketing_department"
    HIRING_OPERATIONS = "hiring_in_operations_department"
    HIRING_PROFESSIONAL = "hiring_in_professional_service_department"
    HIRING_SALES = "hiring_in_sales_department"
    HIRING_SUPPORT = "hiring_in_support_department"
    HIRING_TRADE = "hiring_in_trade_department"
    HIRING_UNKNOWN = "hiring_in_unknown_department"
