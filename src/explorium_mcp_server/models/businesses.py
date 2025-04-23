from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from .shared import BasePaginatedResponse
from .enum_types import CompanyRevenue, CompanyAge, NumberOfLocations


class FetchBusinessesFilters(BaseModel):
    """
      Business search filters.
      Before calling a tool that uses this filter, call the autocomplete tool to get the list of available values,
      especially when using linkedin_category, google_category, naics_category, and region_country_code.
      Only one category can be present at a time (google_category, naics_category, or linkedin_category).
      """

    country_code: Optional[List[str]] = Field(
        default=None,
        description="List of ISO Alpha-2 country codes (e.g., 'US', 'IL') to filter companies by their main headquarters country.",
        examples=[["US", "IL"]]
    )
    region_country_code: Optional[List[str]] = Field(
        default=None,
        description="List of region-country codes (e.g., 'US-CA', 'IL-TA') to filter companies by their specific region.",
        examples=[["US-CA", "IL-TA"]]
    )
    company_size: Optional[List[str]] = Field(
        default=None,
        description="Filter companies based on number of employees (e.g.,'1-10', '51-200').",
        examples=[["11-50", "201-500"]]
    )
    company_revenue: Optional[List[CompanyRevenue]] = Field(
        default=None,
        description="Filter companies by annual revenue range in USD (e.g., '1M-5M', '500M-1B').",
        examples=[["200M-500M", "1B-10B"]]
    )
    company_age: Optional[List[CompanyAge]] = Field(
        default=None,
        description="Filter companies by age since founding (in years).",
        examples=[["0-3", "11-20"]]
    )
    google_category: Optional[List[str]] = Field(
        default=None,
        description="Filter companies by Google industry classification (e.g., 'Retail', 'Construction').",
        examples=[["Retail"]]
    )
    naics_category: Optional[List[str]] = Field(
        default=None,
        description="Filter companies by NAICS industry codes (e.g., '541512' for software services).",
        examples=[["541512", "611310"]]
    )
    linkedin_category: Optional[List[str]] = Field(
        default=None,
        description="Filter companies by LinkedIn industry categories (e.g., 'Market research', 'Software').",
        examples=[["Market research", "Software"]]
    )
    company_tech_stack_category: Optional[List[str]] = Field(
        default=None,
        description="Filter companies by broader technology categories (e.g., 'DevOps and Development', 'Marketing Tools'),"
                    " autocomplete named 'company_tech_stack_categories'.",
        examples=[["DevOps and Development"]]
    )
    company_tech_stack_tech: Optional[List[str]] = Field(
        default=None,
        description="Filter by specific technologies used by the company (e.g., 'Salesforce', 'Amazon RDS').",
        examples=[["Microsoft System Center", "Amazon RDS for MySQL"]]
    )
    company_name: Optional[List[str]] = Field(
        default=None,
        description="Filter companies by exact or partial name match (e.g., 'Google', 'Stripe').",
        examples=[["Microsoft", "Google"]]
    )
    number_of_locations: Optional[List[NumberOfLocations]] = Field(
        default=None,
        description="Filter by how many physical office locations the company has.",
        examples=[["2-5", "101-1000"]]
    )
    city_region_country: Optional[List[str]] = Field(
        default=None,
        description="Filter by location string combining city, region, and country (e.g., 'Tel Aviv, IL', 'Miami, FL, US').",
        examples=[["Tel Aviv, IL", "Miami, FL, US"]]
    )
    website_keywords: Optional[List[str]] = Field(
        default=None,
        description="Filter companies by keywords found on their website (e.g., 'AI', 'ecommerce', 'fintech').",
        examples=[["ecommerce", "retail", "AI"]]
    )


class Business(BaseModel):
    business_id: str
    name: str
    domain: Optional[str] = Field(default=None)
    logo: Optional[str] = Field(default=None)
    country_name: str
    number_of_employees_range: str
    yearly_revenue_range: str
    website: Optional[str] = Field(default=None)
    business_description: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    naics: Optional[int] = Field(default=None)
    naics_description: Optional[str] = Field(default=None)
    sic_code: Optional[str] = Field(default=None)
    sic_code_description: Optional[str] = Field(default=None)


class FetchBusinessesResponse(BasePaginatedResponse):
    data: list[Business]


class MatchBusinessInput(BaseModel):
    """
    Business matching input.

    Provide one or more identifiers to enhance matching accuracy. Use both name and domain when available.
    """

    name: Optional[str] = Field(default=None, description="The business name.")
    domain: Optional[str] = Field(default=None, description="The business domain or website URL.")


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
