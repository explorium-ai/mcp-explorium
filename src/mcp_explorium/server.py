# server.py
from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional, List, Dict, Any
from enum import Enum
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, conlist
import models

# Get API keys from environment variables
load_dotenv()
EXPLORIUM_API_KEY = os.environ.get("EXPLORIUM_API_KEY")
BASE_URL = "https://api.explorium.ai/v1"


def make_api_request(url, payload, headers=None):
    """Helper function to make API requests with consistent error handling"""
    if headers is None:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api_key": EXPLORIUM_API_KEY,
        }

    try:
        serializable_payload = models.utils.pydantic_model_to_serializable(payload)
        response = requests.post(
            f"{BASE_URL}/{url}", json=serializable_payload, headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, "status_code", None),
        }


# Create an MCP server
mcp = FastMCP("Explorium", dependencies=["requests", "pydantic", "dotenv"])


@mcp.tool()
def match_business(business_to_match: models.businesses.MatchBusinessInput):
    """Get the business ID from business name and business domain
    Use this when:
    - Need company size/revenue/industry
    - Analyzing overall business metrics
    - Researching company background


    Do NOT use when:
    - Looking for specific employees
    - Getting executive contact info
    - Finding team member details
    """
    return make_api_request(
        "businesses/match",
        {
            "businesses_to_match": [
                models.utils.pydantic_model_to_serializable(business_to_match)
            ]
        },
    )


@mcp.tool()
def match_businesses_bulk(
    businesses_to_match: conlist(
        models.businesses.MatchBusinessInput, min_length=1, max_length=50
    )
):
    """Get the business IDs from business name and business domain in bulk.
    Use this when:
    - Need company size/revenue/industry
    - Analyzing overall business metrics
    - Researching company background


    Do NOT use when:
    - Looking for specific employees
    - Getting executive contact info
    - Finding team member details
    """
    return make_api_request(
        "businesses/match",
        {
            "businesses_to_match": models.utils.pydantic_model_to_serializable(
                businesses_to_match
            )
        },
    )


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
    return make_api_request(
        "businesses/firmographics/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def enrich_with_technographics(business_id: str) -> Dict[str, Any]:
    """Get company technology stack and digital presence information"""
    return make_api_request(
        "businesses/technographics/enrich",
        {"business_id": business_id},
    )


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
    """Get company strategy insights from 10-K filings - only relevant for public companies, as they have ticker in the firmograpgic"""
    return make_api_request(
        "businesses/pc_strategy_10k/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def enrich_with_business_challenges(business_id):
    """Get business challenges analysis from 10-K filings - only relevant for Public companys, public companiy have ticker in the firmograpgic"""
    return make_api_request(
        "businesses/pc_business_challenges_10k/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def enrich_with_employee_ratings(business_id):
    """Get company ratings and reviews from employees"""
    return make_api_request(
        "businesses/company_ratings_by_employees/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def enrich_with_funding_acquisition(business_id):
    """Get company funding and acquisition history"""
    return make_api_request(
        "businesses/funding_and_acquisition/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def enrich_with_financial_indicators(business_id):
    """Get company financial indicators and metrics"""
    return make_api_request(
        "businesses/financial_indicators/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def enrich_with_website_changes(business_id):
    """Get company website changes and updates history"""
    return make_api_request(
        "businesses/website_changes/enrich",
        {"business_id": business_id},
    )


@mcp.tool()
def fetch_prospects(
    filters: models.prospects.FetchProspectsFilters,
    size: int = Field(
        default=1000, le=1000, description="The number of prospects to return"
    ),
    page_size: int = Field(
        default=100, le=100, description="The number of prospects to return per page"
    ),
    page: int = Field(default=1, description="The page number to return"),
):
    """Get a list of prospects according to the filters.
    If looking for prospects from a specific business, use the business_id filter.
    If you don't have values for business_id, use the match_business or match_business_bulk tool first.

    """

    data = {
        "mode": "full",
        "size": size,
        "page_size": page_size,
        "page": page,
        "filters": models.utils.get_filters_payload(filters),
    }

    return make_api_request("prospects", data)


@mcp.tool()
def match_prospect(prospect_to_match: models.prospects.ProspectMatchInput):
    """Match a prospect with name and company to get the prospect id.
    At least email OR (full name AND company) must be provided.
    """
    # Check if we have at least the required parameters
    if not prospect_to_match.email and (
        not prospect_to_match.full_name or not prospect_to_match.company_name
    ):
        raise ValueError("Either email OR (full name AND company) must be provided")
    return make_api_request(
        "prospects/match",
        {
            "prospects_to_match": [
                models.utils.pydantic_model_to_serializable(prospect_to_match)
            ]
        },
    )


@mcp.tool()
def match_prospects_bulk(
    prospects_to_match: conlist(
        models.prospects.ProspectMatchInput, min_length=1, max_length=40
    )
):
    """Match a list of prospects with name and company to get the prospect id.
    At least email OR (full name AND company) must be provided.
    """
    for prospect_to_match in prospects_to_match:
        if not prospect_to_match.email and (
            not prospect_to_match.full_name or not prospect_to_match.company_name
        ):
            raise ValueError("Either email OR (full name AND company) must be provided")
    return make_api_request(
        "prospects/match",
        {
            "prospects_to_match": [
                models.utils.pydantic_model_to_serializable(prospects_to_match)
            ]
        },
    )


@mcp.tool()
def enrich_prospect_with_social_media(prospect_id: str) -> str:
    """enrich a prospect with linkedin posts the prospect published"""
    return make_api_request(
        "prospects/linkedin_posts/enrich", {"prospect_id": prospect_id}
    )


@mcp.tool()
def enrich_prospect_with_contact_information(prospect_id: str) -> str:
    """enrich a prospect with contact information, use this to add email or phone number to a person.
    show all output in a table - its important.
    """
    return make_api_request(
        "prospects/contacts_information/enrich", {"prospect_id": prospect_id}
    )


@mcp.tool()
def enrich_prospect_with_full_linkedin_profile(prospect_id: str) -> str:
    """enrich a prospect the full linkedin profile including interests, skills and past experience
    show all output in a table - its important
    """
    return make_api_request("prospects/profiles/enrich", {"prospect_id": prospect_id})


@mcp.tool()
def fetch_businesses(
    filters: models.businesses.FetchBusinessesFilters,
    size: int = Field(
        default=1000, le=1000, description="The number of businesses to return"
    ),
    page_size: int = Field(
        default=100, le=100, description="The number of businesses to return per page"
    ),
    page: int = Field(default=1, description="The page number to return"),
) -> models.businesses.FetchBusinessesResponse:
    """
    Fetch businesses from the Explorium API filtered by various criteria.
    """
    # Prepare request payload
    payload = {
        "mode": "full",
        "size": size,
        "page_size": page_size,
        "page": page,
        "filters": models.utils.get_filters_payload(filters),
        "request_context": {},
    }

    return make_api_request("businesses", payload)


@mcp.tool()
def generata_pipeline_from_conversation(full_context: str):
    """generate data pipeline based on all context (full conversation history including tools input output)
    make sure to add ALL tool invockion including input and output.
    """

    return full_context


@mcp.tool()
def fetch_business_events(
    business_ids: List[str],
    event_types: List[models.businesses.BusinessEventType],
    timestamp_from: str = Field(description="ISO 8601 timestamp"),
    timestamp_to: str | None = Field(default=None, description="ISO 8601 timestamp"),
) -> Dict[str, Any]:
    """
    Retrieves business-related events from the Explorium API.

    This function fetches various business events such as funding rounds,
    IPO announcements, new offices, and job market shifts.
    """
    # Basic validation
    if not business_ids:
        raise ValueError("business_ids cannot be empty")

    if not event_types:
        raise ValueError("event_types cannot be empty")

    # Prepare request
    payload = {
        "event_types": models.utils.enum_list_to_serializable(event_types),
        "business_ids": business_ids,
        "timestamp_from": timestamp_from,
    }

    if timestamp_to:
        payload["timestamp_to"] = timestamp_to

    return make_api_request("businesses/events", payload)


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
