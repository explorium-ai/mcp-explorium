# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional, List
from typing import List, Dict, Optional, Any
from enum import Enum
import os
from dotenv import load_dotenv

# Get API keys from environment variables
load_dotenv()
EXPLORIUM_API_KEY = os.environ.get("EXPLORIUM_API_KEY")


# Create an MCP server
mcp = FastMCP("Prospecting", dependencies=["requests", "pydantic", "dotenv"])


@mcp.tool()
def match_business(name, domain):
    """Get the business ID from business name and business domain
    Use this when:
    - Need company size/revenue/industry
    - Analyzing overall business metrics
    - Researching company background


    Do NOT use when:
    - Looking for specific employees
    - Getting executive contact info
    - Finding team member details"
    """
    url = "https://api.explorium.ai/v1/businesses/match"
    headers = {"API_KEY": EXPLORIUM_API_KEY, "Content-Type": "application/json"}
    data = {
        "businesses_to_match": [
            {"name": name, "domain": domain},
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()


@mcp.tool()
def enrich_with_company_profile(business_id):
    """Get company firmographic information including size, industry, revenue but NOT C-level
    Use this when:
    - Need company size/revenue/industry
    - Analyzing overall business metrics
    - Researching company background


    Do NOT use when:
    - Looking for specific employees
    - Getting executive contact info
    - Finding team member details
    """
    url = "https://api.explorium.ai/v1/businesses/firmographics/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_technographics(business_id):
    """Get company technology stack and digital presence information"""
    url = "https://api.explorium.ai/v1/businesses/technographics/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_social_media(business_id):
    """Get company LinkedIn posts and social media presence"""
    url = "https://api.explorium.ai/v1/businesses/linkedin_posts/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_workforce_trends(business_id):
    """Get company workforce trends and employment data"""
    url = "https://api.explorium.ai/v1/businesses/workforce_trends/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_competitive_landscape(business_id):
    """Get competitive landscape analysis from 10-K filings - only relevant for Public companys, public companiy have ticker in the firmograpgic"""
    url = "https://api.explorium.ai/v1/businesses/pc_competitive_landscape_10k/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_strategy(business_id):
    """Get company strategy insights from 10-K filings - only relevant for Public companys, public companiy have ticker in the firmograpgic"""
    url = "https://api.explorium.ai/v1/businesses/pc_strategy_10k/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_business_challenges(business_id):
    """Get business challenges analysis from 10-K filings - only relevant for Public companys, public companiy have ticker in the firmograpgic"""
    url = "https://api.explorium.ai/v1/businesses/pc_business_challenges_10k/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_employee_ratings(business_id):
    """Get company ratings and reviews from employees"""
    url = "https://api.explorium.ai/v1/businesses/company_ratings_by_employees/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_funding_acquisition(business_id):
    """Get company funding and acquisition history"""
    url = "https://api.explorium.ai/v1/businesses/funding_and_acquisition/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_financial_indicators(business_id):
    """Get company financial indicators and metrics"""
    url = "https://api.explorium.ai/v1/businesses/financial_indicators/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_with_website_changes(business_id):
    """Get company website changes and updates history"""
    url = "https://api.explorium.ai/v1/businesses/website_changes/enrich"
    payload = {"business_id": business_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


# start
from pydantic import BaseModel, Field


# Define JobLevel Enum
class JobLevel(str, Enum):
    DIRECTOR = "Director"
    MANAGER = "Manager"
    VP = "Vp"
    PARTNER = "Partner"
    CXO = "Cxo"
    NON_MANAGERIAL = "Non-managerial"
    SENIOR = "Senior"
    ENTRY = "Entry"
    TRAINING = "Training"
    UNPAID = "Unpaid"


# Define JobDepartment Enum
class JobDepartment(str, Enum):
    CUSTOMER_SERVICE = "Customer service"
    DESIGN = "Design"
    EDUCATION = "Education"
    ENGINEERING = "Engineering"
    FINANCE = "Finance"
    GENERAL = "General"
    HEALTH = "Health"
    HUMAN_RESOURCES = "Human resources"
    LEGAL = "Legal"
    MARKETING = "Marketing"
    MEDIA = "Media"
    OPERATIONS = "Operations"
    PUBLIC_RELATIONS = "Public relations"
    REAL_ESTATE = "Real estate"
    SALES = "Sales"
    TRADES = "Trades"
    UNKNOWN = "Unknown"


# Define Request Model using Pydantic
class ProspectFilter(BaseModel):
    size: int = 5
    job_departments: Optional[List[JobDepartment]] = None
    job_level: Optional[List[JobLevel]] = None
    business_id: Optional[str] = None


@mcp.tool()
def fetch_prospects_with_filters(filters: ProspectFilter):
    """Get a list of prospects according to the filters

    Filters:
    - Job level: Filters by job level as list. Options: Director, Manager, Vp, Partner, Cxo, Non-managerial, Senior, Entry, Training, Unpaid.
    - Job department: Filters by job department as list. Options: Customer service, Design, Education, Engineering, Finance, General, Health, Human resources, Legal, Marketing, Media, Operations, Public relations, Real estate, Sales, Trades, Unknown.
    """
    # API URL
    url = "https://api.explorium.ai/v1/prospects"

    # API Key
    headers = {"API_KEY": EXPLORIUM_API_KEY, "Content-Type": "application/json"}

    # Payload with filters
    filters_payload = {}

    if filters.job_level:
        filters_payload["job_level"] = {
            "type": "includes",
            "values": [level.value for level in filters.job_level],
        }

    if filters.job_departments:
        filters_payload["job_department"] = {
            "type": "includes",
            "values": [dept.value for dept in filters.job_departments],
        }

    if filters.business_id:
        filters_payload["business_id"] = {
            "type": "includes",
            "values": [filters.business_id],
        }

    data = {
        "mode": "full",
        "size": filters.size,
        "page_size": filters.size,
        "filters": filters_payload,
    }

    # Send request using json parameter instead of str()
    response = requests.post(url, headers=headers, json=data)

    # Return response
    return response.json()


# end


@mcp.tool(description="fetch_prospects")
def fetch_prospects(
    size=5,
    job_departments: Optional[List[str]] = None,
    job_level: Optional[List[str]] = None,
    business_id: Optional[str] = None,
):
    """get a list of prospect according to the filters
     Filters:
    - Job level: Filters by job level as list. Options: Director, Manager, Vp, Partner, Cxo, Non-managerial, Senior, Entry, Training, Unpaid.
    - Job department: Filters by job department as list. Options: Customer service, Design, Education, Engineering, Finance, General, Health, Human resources, Legal, Marketing, Media, Operations, Public relations, Real estate, Sales, Trades, Unknown.
    """
    # API URL
    url = "https://api.explorium.ai/v1/prospects"

    # API Key
    headers = {"API_KEY": EXPLORIUM_API_KEY, "Content-Type": "application/json"}

    # Payload with filters
    filters = {}

    if job_level:
        filters["job_level"] = {"type": "includes", "values": job_level}

    if job_departments:
        filters["job_department"] = {"type": "includes", "values": job_departments}

    if business_id:
        filters["business_id"] = {"type": "includes", "values": [business_id]}

    data = {"mode": "full", "size": size, "page_size": 1, "filters": filters}

    # Send request using json parameter instead of str()
    response = requests.post(url, headers=headers, json=data)

    # Return response
    return response.json()


@mcp.tool()
def match_prospect_and_get_prospect_id(
    prospect_full_name: Optional[str] = None,
    prospects_company: Optional[str] = None,
    email: Optional[str] = None,
) -> str:
    """match a prospect with name and company to get the prospect id.
    Prospect ID is than can be used to further enrich the prospect.
    Can also match using email address.

    At least email OR (full name AND company) must be provided.
    """
    # Check if we have at least the required parameters
    if not email and (not prospect_full_name or not prospects_company):
        raise ValueError("Either email OR (full name AND company) must be provided")

    url = "https://api.explorium.ai/v1/prospects/match"

    # Create the prospect object based on provided parameters
    prospect_obj = {}

    if email:
        prospect_obj["email"] = email

    if prospect_full_name:
        prospect_obj["full_name"] = prospect_full_name

    if prospects_company:
        prospect_obj["company_name"] = prospects_company

    payload = {"prospects_to_match": [prospect_obj]}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@mcp.tool()
def enrich_prospect_with_social_media(prospect_id: str) -> str:
    """enrich a prospect with linkedin posts the prospect published"""
    url = "https://api.explorium.ai/v1/prospects/linkedin_posts/enrich"
    payload = {"prospect_id": prospect_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)

    # Return response
    return response.json()


@mcp.tool()
def enrich_prospect_with_contact_information(prospect_id: str) -> str:
    """enrich a prospect with contact information, use this to add email or phone number to a person.
    show all output in a table - its important.
    """
    url = "https://api.explorium.ai/v1/prospects/contacts_information/enrich"
    payload = {"prospect_id": prospect_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)

    # Return response
    return response.json()


@mcp.tool()
def enrich_prospect_with_full_linkedin_profile(prospect_id: str) -> str:
    """enrich a prospect the full linkedin profile including interests, skills and past experience
    show all output in a table - its important
    """
    url = "https://api.explorium.ai/v1/prospects/profiles/enrich"
    payload = {"prospect_id": prospect_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }

    response = requests.post(url, json=payload, headers=headers)

    # Return response
    return response.json()


@mcp.prompt()
def write_cold_outreach_email(
    company_website: str, target_company_domain: str, target_person_full_name: str
) -> str:
    """define the steps necessary to write a cold email outreach"""
    prompt = f"""
       Objective:
Craft a highly personalized cold email to a potential prospect by leveraging insights about my company,
the target company, and the recipient. The goal is to identify their potential need for my product by referencing relevant company events,
industry trends, and personal interests.
After every research step and especially before writing the email create a short summery to the user to show him what you have learned.
Inputs:
My company's website: {company_website}
Target company's name: {target_company_domain}
Target person's name: {target_person_full_name}
Research Steps:
1. Understand My Company
Analyze {company_website} and conduct a company research to understand my business, product offerings, and unique value proposition.
Identify key benefits and differentiators that are particularly relevant to {target_company_domain}.
2. Research the Target Company ({target_company_domain})
Gather insights from news articles, company updates, job postings, and other publicly available data.
- Use match_business to get company ID
- Use enrich_with_company_profile for firmographic data (size, revenue, industry)
- Use enrich_with_technographics to understand their tech stack
- Use enrich_with_social_media for social presence analysis
- Use enrich_with_workforce_trends to analyze hiring patterns
- Use enrich_with_company_linkedin_posts for recent announcements
- Use enrich_with_website_changes to detect positioning shifts
- If public company, use:
 * enrich_with_competitive_landscape
 * enrich_with_strategy
 * enrich_with_business_challenges
- Use enrich_with_funding_acquisition for growth insights
- Use enrich_with_financial_indicators for business health
- Use search and news functions for recent developments


Example:
If the company recently experienced a data breach (for a cybersecurity product) or is expanding its sales team (for a sales enablement tool), incorporate these insights into the email.


3. Research {target_person_full_name}
Examine their LinkedIn profile for past experiences, skills, and shared content.
Identify their personal interests, industry expertise, and any posts they've engaged with that align with my product's value.




Cold Email Requirements:
Length: No more than two paragraphs.
Opening: Personalize it by referencing a relevant event or insight about {target_company_domain} or {target_person_full_name}.
Value Proposition: Clearly and concisely explain how my product can address their needs or challenges.
Call to Action: End with a soft close, e.g., "Would love to hear your thoughts – open to a quick chat next week?"
Expected Output:
A concise, engaging, and highly relevant cold email that captures the recipient's attention and demonstrates why my product is valuable to them.


   """
    return prompt


from enum import Enum
from typing import Dict, List, Optional, Any
import requests


# API key is assumed to be defined elsewhere as EXPLORIUM_API_KEY


class CompanySize(str, Enum):
    """All available company size ranges"""

    SIZE_1_10 = "1-10"
    SIZE_11_50 = "11-50"
    SIZE_51_200 = "51-200"
    SIZE_201_500 = "201-500"
    SIZE_501_1000 = "501-1000"
    SIZE_1001_5000 = "1001-5000"
    SIZE_5001_10000 = "5001-10000"
    SIZE_10001_PLUS = "10001+"


class CompanyRevenue(str, Enum):
    """All available company revenue ranges"""

    REV_0_1M = "0-1M"
    REV_1M_5M = "1M-5M"
    REV_5M_10M = "5M-10M"
    REV_10M_50M = "10M-50M"
    REV_50M_100M = "50M-100M"
    REV_100M_500M = "100M-500M"
    REV_500M_1B = "500M-1B"
    REV_1B_10B = "1B-10B"
    REV_10B_100B = "10B-100B"


class CompanyAge(str, Enum):
    """All available company age ranges"""

    AGE_0_3 = "0-3"
    AGE_4_10 = "4-10"
    AGE_11_20 = "11-20"
    AGE_20_PLUS = "20+"


@mcp.tool()
def fetch_businesses(
    company_sizes: Optional[List[CompanySize]] = None,
    company_revenues: Optional[List[CompanyRevenue]] = None,
    country_code: Optional[str] = None,
    region_country_code: Optional[str] = None,
    company_age: Optional[List[CompanyAge]] = None,
    google_category: Optional[List[str]] = None,
    naics_category: Optional[List[str]] = None,
    linkedin_category: Optional[List[str]] = None,
    size: int = 10,
    page_size: int = 100,
    page: int = 1,
) -> Dict[str, Any]:
    """
    Fetch businesses from the Explorium API filtered by various criteria.

    Args:
        company_sizes (List[CompanySize], optional): List of company size ranges. Available options:
            - SIZE_1_10: "1-10 employees"
            - SIZE_11_50: "11-50 employees"
            - SIZE_51_200: "51-200 employees"
            - SIZE_201_500: "201-500 employees"
            - SIZE_501_1000: "501-1000 employees"
            - SIZE_1001_5000: "1001-5000 employees"
            - SIZE_5001_10000: "5001-10000 employees"
            - SIZE_10001_PLUS: "10001+ employees"

        company_revenues (List[CompanyRevenue], optional): List of company revenue ranges. Available options:
            - REV_0_1M: "$0-1M annual revenue"
            - REV_1M_5M: "$1M-5M annual revenue"
            - REV_5M_10M: "$5M-10M annual revenue"
            - REV_10M_50M: "$10M-50M annual revenue"
            - REV_50M_100M: "$50M-100M annual revenue"
            - REV_100M_500M: "$100M-500M annual revenue"
            - REV_500M_1B: "$500M-1B annual revenue"
            - REV_1B_10B: "$1B-10B annual revenue"
            - REV_10B_100B: "$10B-100B annual revenue"

        country_code (str, optional): Filters businesses by country (e.g., "us", "ca")

        region_country_code (str, optional): Filters businesses by specific regions within countries (e.g., "us-ca")

        company_age (List[CompanyAge], optional): List of company age ranges. Available options:
            - AGE_0_3: "0-3 years"
            - AGE_4_10: "4-10 years"
            - AGE_11_20: "11-20 years"
            - AGE_20_PLUS: "20+ years"

        google_category (List[str], optional): Filters by Google's classification (e.g., "retail", "consulting")

        naics_category (List[str], optional): Filters by NAICS industry classification (e.g., "23", "5611")

        linkedin_category (List[str], optional): Filters by LinkedIn industry classification (e.g., "software development")

        size (int): Maximum number of results to return (max 1000)
        page_size (int): Maximum number of records per page (max 100)
        page (int): Page number to retrieve

    Returns:
        Dict[str, Any]: API response containing:
            - total_results: Total number of matching businesses
            - page: Current page number
            - total_pages: Total number of pages
            - data: List of business records with fields:
                - name: Company name
                - domain: Company website domain
                - number_of_employees: Employee count range
                - yearly_revenue: Annual revenue range

    Raises:
        ValueError: If size > 1000 or page_size > 100
        requests.RequestException: If the API request fails

    """
    if size > 1000:
        raise ValueError("Maximum size is 1000")
    if page_size > 100:
        raise ValueError("Maximum page_size is 100")

    # Build filters dictionary
    filters = {}

    if company_sizes:
        filters["company_size"] = {
            "type": "includes",
            "values": [size.value for size in company_sizes],
        }

    if company_revenues:
        filters["company_revenue"] = {
            "type": "includes",
            "values": [rev.value for rev in company_revenues],
        }

    if country_code:
        filters["country_code"] = {"type": "includes", "values": [country_code]}

    if region_country_code:
        filters["region_country_code"] = {
            "type": "includes",
            "values": [region_country_code],
        }

    if company_age:
        filters["company_age"] = {
            "type": "includes",
            "values": [age.value for age in company_age],
        }

    if google_category:
        filters["google_category"] = {"type": "includes", "values": google_category}

    if naics_category:
        filters["naics_category"] = {"type": "includes", "values": naics_category}

    if linkedin_category:
        filters["linkedin_category"] = {"type": "includes", "values": linkedin_category}

    # Prepare request payload
    payload = {
        "mode": "full",
        "size": size,
        "page_size": page_size,
        "page": page,
        "filters": filters,
        "request_context": {},
    }

    # Make API request
    headers = {"API_KEY": EXPLORIUM_API_KEY, "Content-Type": "application/json"}

    response = requests.post(
        f"https://api.explorium.ai/v1/businesses", headers=headers, json=payload
    )

    response.raise_for_status()
    return response.json()


@mcp.tool()
def generata_pipeline_from_conversation(full_context: str):
    """generate data pipeline based on all context (full conversation history including tools input output)
    make sure to add ALL tool invockion including input and output.
    """

    return full_context


class EventType(str, Enum):
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


@mcp.tool()
def fetch_business_events(
    business_id: str,
    event_types: List[EventType],
    timestamp_from: str,
    timestamp_to: Optional[str] = None,
) -> Dict[str, Any]:
    """
       Retrieves business-related events from the Explorium API.

       This function fetches various business events such as funding rounds,
       IPO announcements, new offices, and job market shifts.
       Organizational Announcements


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
    Hiring in Unknown Department: Recruiting where department is not specified



       Args:
           business_id (str): Business ID to fetch events for
           event_types (List[EventType]): Types of events to retrieve from EventType enum
           timestamp_from (str): Return only events after this timestamp (ISO format)
           timestamp_to (str, optional): Return only events before this timestamp (ISO format)

       Returns:
           Dict[str, Any]: Response containing event information

       Raises:
           ValueError: If invalid parameters are provided
           requests.RequestException: If the API request fails


    """
    # Basic validation
    if not business_id:
        raise ValueError("business_id cannot be empty")

    if not event_types:
        raise ValueError("event_types cannot be empty")

    # Prepare request
    url = "https://api.explorium.ai/v1/businesses/events"

    headers = {"API_KEY": EXPLORIUM_API_KEY, "Content-Type": "application/json"}

    payload = {
        "event_types": [et.value for et in event_types],
        "business_ids": [business_id],
        "timestamp_from": timestamp_from,
    }

    if timestamp_to:
        payload["timestamp_to"] = timestamp_to

    # Make request
    response = requests.post(url, headers=headers, json=payload)

    # Handle response
    if response.status_code != 200:
        raise requests.RequestException(
            f"API request failed with status code {response.status_code}: {response.text}"
        )

    return response.json()
