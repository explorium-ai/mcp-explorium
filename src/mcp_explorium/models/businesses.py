from pydantic import BaseModel, Field
from typing import Literal, Optional
from enum import Enum
from ._shared import BasePaginatedResponse


# Fetch Businesses Filters
class CompanySize(str, Enum):
    """All available company size ranges.
    Possible values:
    SIZE_1_10: 1-10 employees
    SIZE_11_50: 11-50 employees
    SIZE_51_200: 51-200 employees
    SIZE_201_500: 201-500 employees
    SIZE_501_1000: 501-1000 employees
    SIZE_1001_5000: 1001-5000 employees
    SIZE_5001_10000: 5001-10000 employees
    SIZE_10001_PLUS: 10001+ employees

    """

    SIZE_1_10 = "1-10"
    SIZE_11_50 = "11-50"
    SIZE_51_200 = "51-200"
    SIZE_201_500 = "201-500"
    SIZE_501_1000 = "501-1000"
    SIZE_1001_5000 = "1001-5000"
    SIZE_5001_10000 = "5001-10000"
    SIZE_10001_PLUS = "10001+"


class CompanyRevenue(str, Enum):
    """
    All available revenue ranges in annual $:
    REV_0_500K: $0-500K yearly revenue
    REV_500K_1M: $500k-1M yearly revenue
    REV_1M_5M: $1M-5M yearly revenue
    REV_5M_10M: $5M-10M yearly revenue
    REV_10M_25M: $10M-25M yearly revenue
    REV_25M_75M: $25M-75M yearly revenue
    REV_75M_200M: $75M-200M yearly revenue
    REV_200M_500M: $200M-500M yearly revenue
    REV_500M_1B: $500M-1B yearly revenue
    REV_1B_10B: $1B-10B yearly revenue
    REV_10B_100B: $10B-100B yearly revenue
    REV_100B_1T: $100B-1T yearly revenue
    REV_1T_10T: $1T-10T yearly revenue
    REV_10T_PLUS: $10T+ yearly revenue
    """

    REV_0_500K = "0-500K"
    REV_500K_1M = "500k-1M"
    REV_1M_5M = "1M-5M"
    REV_5M_10M = "5M-10M"
    REV_10M_25M = "10M-25M"
    REV_25M_75M = "25M-75M"
    REV_75M_200M = "75M-200M"
    REV_200M_500M = "200M-500M"
    REV_500M_1B = "500M-1B"
    REV_1B_10B = "1B-10B"
    REV_10B_100B = "10B-100B"
    REV_100B_1T = "100B-1T"
    REV_1T_10T = "1T-10T"
    REV_10T_PLUS = "10T+"


class CompanyAge(str, Enum):
    """All available company age ranges in years:
    AGE_0_3: 0-3 years
    AGE_4_10: 4-10 years
    AGE_11_20: 11-20 years
    AGE_20_PLUS: 20+ years
    """

    AGE_0_3 = "0-3"
    AGE_4_10 = "4-10"
    AGE_11_20 = "11-20"
    AGE_20_PLUS = "20+"


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
    """Input for matching businesses. Use multiple identifiers for higher match accuracy."""

    name: Optional[str]
    domain: Optional[str]


class BusinessEventType(str, Enum):
    """Valid event types for the Explorium Business Events API.
    A full list of supported events:
    IPO Announcement: Company announces plans to go public through an initial public offering
    New Funding Round: Company secures a new round of investment funding
    New Investment: Company makes an investment in another business or venture
    New Product: Company launches a new product or service
    New Office: Company opens a new office location
    Closing Office: Company closes an existing office location
    New Partnership: Company forms a strategic partnership with another organization


    Department Growth
    Increase in Engineering Department: Expansion of the engineering team
    Increase in Sales Department: Growth in the sales team
    Increase in Marketing Department: Expansion of the marketing team
    Increase in Operations Department: Growth in operations staff
    Increase in Customer Service Department: Expansion of customer service team
    Increase in All Departments: Company-wide growth across all departments


    Department Reduction
    Decrease in Engineering Department: Reduction in engineering team size
    Decrease in Sales Department: Reduction in sales team size
    Decrease in Marketing Department: Reduction in marketing team size
    Decrease in Operations Department: Reduction in operations staff
    Decrease in Customer Service Department: Reduction in customer service team
    Decrease in All Departments: Company-wide reduction across all departments


    Hiring Initiatives
    Employee Joined Company: Individual hire announcement
    Hiring in Creative Department: Recruiting for creative roles
    Hiring in Education Department: Recruiting for education-related positions
    Hiring in Engineering Department: Recruiting for engineering and technical roles
    Hiring in Finance Department: Recruiting for financial positions
    Hiring in Health Department: Recruiting for healthcare-related roles
    Hiring in Human Resources Department: Recruiting for HR positions
    Hiring in Legal Department: Recruiting for legal team
    Hiring in Marketing Department: Recruiting for marketing roles
    Hiring in Operations Department: Recruiting for operations positions
    Hiring in Professional Service Department: Recruiting for professional services
    Hiring in Sales Department: Recruiting for sales positions
    Hiring in Support Department: Recruiting for customer support roles
    Hiring in Trade Department: Recruiting for trade-related positions
    Hiring in Unknown Department: Recruiting where department is not specified"""

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
