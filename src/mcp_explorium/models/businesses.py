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
    """
    Business search filters.
    Before calling a tool that uses this filter, call the autocomplete tool to get the list of available values,
    especially when using linkedin_category, google_category, naics_category, and region_country_code.
    Only one category can be present at a time (google_category, naics_category, or linkedin_category).
    """

    country_code: None | list[str] = Field(
        default=None,
        description="A list of lowercase two-letter ISO country codes.",
    )
    region_country_code: None | list[str] = Field(
        default=None,
        description="A list of lowercase region-country codes in the format 'REGION-CC' where CC is the two-letter ISO country code.",
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
        description="Filters accounts by categories as classified in Google.",
    )
    naics_category: None | list[str] = Field(
        default=None,
        description='Filters accounts by the North American Industry Classification System categories. Example: ["23", "5611"]',
    )
    linkedin_category: None | list[str] = Field(
        default=None,
        description="Filters accounts by categories as used in LinkedIn.",
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
    """
    Valid event types for the Explorium Business Events API.

    IPO_ANNOUNCEMENT: Company announces plans to go public through an initial public offering
    - link: str - Link to article
    - ipo_date: datetime - Date of IPO
    - event_id: str - News event ID
    - company_name: str - Company name
    - offer_amount: float - Company valuation
    - number_of_shares: int - Number of issued shares
    - stock_exchange: str - IPO stock exchange
    - event_time: datetime - News event timestamp
    - price_per_share: float - Price per share
    - ticker: str - Ticker

    NEW_FUNDING_ROUND: Company secures a new round of investment funding
    - founding_date: datetime - Date of funding round
    - amount_raised: float - Amount raised in funding
    - link: str - Link to article
    - founding_stage: str - Funding round stage
    - event_id: str - News event ID
    - event_time: datetime - News event timestamp
    - investors: str - Investors in funding round
    - lead_investor: str - Lead investor

    NEW_INVESTMENT: Company makes an investment in another business or venture
    - investment_date: datetime - News event timestamp
    - investment_type: str - Type of investment
    - event_time: datetime - News report publishing date
    - event_id: str - News event ID
    - investment_target: str - Target of investment
    - link: str - Link to article
    - investment_amount: float - Amount of investment

    NEW_PRODUCT: Company launches a new product or service
    - event_time: datetime - News event timestamp
    - event_id: str - News event ID
    - link: str - Link to article
    - product_name: str - Name of new product
    - product_description: str - Description of new product
    - product_category: str - Category of new product
    - product_launch_date: datetime - Launch date of new product

    NEW_OFFICE: Company opens a new office location
    - purpose_of_new_office: str - Purpose of new office
    - link: str - Link to article
    - opening_date: datetime - Date of office opening
    - event_id: str - News event ID
    - office_location: str - Location of new office
    - event_time: datetime - News report publishing date
    - number_of_employees: int - Number of employees at new office

    CLOSING_OFFICE: Company closes an existing office location
    - reason_for_closure: str - Reason for office closing
    - event_time: datetime - News report publishing date
    - office_location: str - Location of closing office
    - closure_date: datetime - Date of office closing
    - event_id: str - News event ID
    - number_of_employees_affected: int - Number of employees impacted
    - link: str - Link to article

    NEW_PARTNERSHIP: Company forms a strategic partnership with another organization
    - link: str - Link to article
    - partner_company: str - Name of partnering company
    - partnership_date: datetime - Date of partnership
    - event_time: datetime - News report publishing date
    - purpose_of_partnership: str - Partnership purpose
    - event_id: str - News event ID

    DEPARTMENT_INCREASE_*: Company announces an increase in a specific department
    DEPARTMENT_DECREASE_*: Company announces a decrease in a specific department
    Possible input departments: ENGINEERING, SALES, MARKETING, OPERATIONS, CUSTOMER_SERVICE, ALL
    - department_change: float - Quarterly change in department headcount
    - event_time: datetime - Department event timestamp
    - event_id: str - Department event ID
    - quarter_partition: str - Quarter when change occurred
    - insertion_time: str - Event collection timestamp
    - department: str - Name of department
    - change_type: str - Type of department change

    DEPARTMENT_HIRING_*: Company announces a hiring initiative in a specific department
    Possible input departments: CREATIVE, EDUCATION, ENGINEERING, FINANCE, HEALTH, HR, LEGAL, MARKETING, OPERATIONS, PROFESSIONAL, SALES, SUPPORT, TRADE, UNKNOWN
    - location: str - Location of hiring initiative
    - event_id: str - Company hiring event ID
    - event_time: datetime - When role was published
    - job_count: int - Number of open positions
    - job_titles: str - Job titles being hired for
    - department: str - Department hiring is occurring in

    EMPLOYEE_JOINED: Employee is hired by an organization
    - job_department: str - Employee's current job department
    - full_name: str - Employee's full name
    - job_role_title: str - Employee's current job title
    - event_id: str - Employee's event ID
    - linkedin_url: str - Employee's LinkedIn URL
    """

    IPO_ANNOUNCEMENT = "ipo_announcement"
    NEW_FUNDING_ROUND = "new_funding_round"
    NEW_INVESTMENT = "new_investment"
    NEW_PRODUCT = "new_product"
    NEW_OFFICE = "new_office"
    CLOSING_OFFICE = "closing_office"
    NEW_PARTNERSHIP = "new_partnership"

    # Department increases
    DEPARTMENT_INCREASE_ENGINEERING = "increase_in_engineering_department"
    DEPARTMENT_INCREASE_SALES = "increase_in_sales_department"
    DEPARTMENT_INCREASE_MARKETING = "increase_in_marketing_department"
    DEPARTMENT_INCREASE_OPERATIONS = "increase_in_operations_department"
    DEPARTMENT_INCREASE_CUSTOMER_SERVICE = "increase_in_customer_service_department"
    DEPARTMENT_INCREASE_ALL = "increase_in_all_departments"

    # Department decreases
    DEPARTMENT_DECREASE_ENGINEERING = "decrease_in_engineering_department"
    DEPARTMENT_DECREASE_SALES = "decrease_in_sales_department"
    DEPARTMENT_DECREASE_MARKETING = "decrease_in_marketing_department"
    DEPARTMENT_DECREASE_OPERATIONS = "decrease_in_operations_department"
    DEPARTMENT_DECREASE_CUSTOMER_SERVICE = "decrease_in_customer_service_department"
    DEPARTMENT_DECREASE_ALL = "decrease_in_all_departments"

    # Hiring events
    EMPLOYEE_JOINED = "employee_joined_company"
    DEPARTMENT_HIRING_CREATIVE = "hiring_in_creative_department"
    DEPARTMENT_HIRING_EDUCATION = "hiring_in_education_department"
    DEPARTMENT_HIRING_ENGINEERING = "hiring_in_engineering_department"
    DEPARTMENT_HIRING_FINANCE = "hiring_in_finance_department"
    DEPARTMENT_HIRING_HEALTH = "hiring_in_health_department"
    DEPARTMENT_HIRING_HR = "hiring_in_human_resources_department"
    DEPARTMENT_HIRING_LEGAL = "hiring_in_legal_department"
    DEPARTMENT_HIRING_MARKETING = "hiring_in_marketing_department"
    DEPARTMENT_HIRING_OPERATIONS = "hiring_in_operations_department"
    DEPARTMENT_HIRING_PROFESSIONAL = "hiring_in_professional_service_department"
    DEPARTMENT_HIRING_SALES = "hiring_in_sales_department"
    DEPARTMENT_HIRING_SUPPORT = "hiring_in_support_department"
    DEPARTMENT_HIRING_TRADE = "hiring_in_trade_department"
    DEPARTMENT_HIRING_UNKNOWN = "hiring_in_unknown_department"
