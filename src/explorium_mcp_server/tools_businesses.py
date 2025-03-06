from . import _shared
from ._shared import (
    mcp,
    make_api_request,
    enum_list_to_serializable,
    get_filters_payload,
    BASE_URL,
    EXPLORIUM_API_KEY,
)
from . import models
from pydantic import conlist, Field
from typing import List, Dict, Any, Literal
from functools import partial

business_ids_field = partial(
    Field, description="List of Explorium business IDs from match_businesses"
)


@mcp.tool()
def match_businesses(
    businesses_to_match: conlist(
        models.businesses.MatchBusinessInput, min_length=1, max_length=50
    )
):
    """
    Get the Explorium business IDs from business name and/or domain in bulk.
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
        {"businesses_to_match": businesses_to_match},
    )


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
):
    """
    Fetch businesses from the Explorium API filtered by various criteria.
    You MUST call the autocomplete tool to get the list of possible values for
    filters specified in the autocomplete tool's description.

    Do NOT use this tool first if you do not have a list of available values for
    mandatory filters specified in the autocomplete tool's description.

    This tool returns Business IDs, which can be used to fetch more information.
    Do NOT call match_businesses afterwards if the response already contains
    business IDs.
    """
    payload = {
        "mode": "full",
        "size": size,
        "page_size": page_size,
        "page": page,
        "filters": get_filters_payload(filters),
        "request_context": {},
    }

    return make_api_request("businesses", payload)


import requests


@mcp.tool()
def autocomplete(
    field: Literal[
        "country",
        "country_code",
        "region_country_code",
        "google_category",
        "naics_category",
        "linkedin_category",
        "company_tech_stack_tech",
        "job_title",
        "company_size",
        "company_revenue",
        "company_age",
        "job_department",
        "job_level",
    ],
    query: str | int = Field(description="The query to autocomplete"),
):
    """
    Autocomplete values for various business fields based on a query string.
    You MUST call this tool before using any of the following filters:
    - linkedin_category
    - google_category
    - naics_category
    - region_country_code

    Do NOT use this tool if you already have a list of available values
    for emum fields, such as:
    - company_size
    - company_age
    - company_revenue

    Hints:
    - When looking for 'saas' in categories, use 'software'
    """
    headers = {
        "accept": "application/json",
        "api_key": EXPLORIUM_API_KEY,
    }

    response = requests.get(
        f"{BASE_URL}/businesses/autocomplete",
        headers=headers,
        params={"field": field, "query": query},
    )
    return response.json()


@mcp.tool()
def fetch_businesses_events(
    business_ids: conlist(str, min_length=1, max_length=20) = business_ids_field(),
    event_types: List[models.businesses.BusinessEventType] = Field(
        description="List of event types to fetch"
    ),
    timestamp_from: str = Field(description="ISO 8601 timestamp"),
    # TODO: This is not implemented yet
    # timestamp_to: str | None = Field(default=None, description="ISO 8601 timestamp"),
) -> Dict[str, Any]:
    """
    Retrieves business-related events from the Explorium API in bulk.
    If you're looking for events related to role changes, you should use the
    prospects events tool instead.
    """
    payload = {
        "business_ids": business_ids,
        "event_types": enum_list_to_serializable(event_types),
        "timestamp_from": timestamp_from,
    }

    # if timestamp_to:
    #     payload["timestamp_to"] = timestamp_to

    return make_api_request("businesses/events", payload)


@mcp.tool()
def fetch_businesses_statistics(
    filters: models.businesses.FetchBusinessesFilters,
):
    """
    Fetch aggregated insights into businesses by industry, revenue, employee count, and geographic distribution.
    """
    return make_api_request(
        "businesses/stats",
        {"filters": get_filters_payload(filters)},
    )


# Enrichment tools


@mcp.tool()
def enrich_businesses_firmographics(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get firmographics data in bulk.
    Returns:
    - Business ID and name
    - Detailed business description
    - Website URL
    - Geographic information (country, region)
    - Industry classification (NAICS code and description)
    - SIC code and description
    - Stock ticker symbol (for public companies)
    - Company size (number of employees range)
    - Annual revenue range
    - LinkedIn industry category and profile URL
    """
    return make_api_request(
        "businesses/firmographics/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_technographics(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get technographics data in bulk.
    Returns:
    - Full technology stack used by the business
    - Nested technology stack categorized by function (e.g., Sales, Marketing, DevOps)
    - Detailed breakdown by categories including:
      - Testing and QA tools
      - Sales software
      - Programming languages and frameworks
      - Productivity and operations tools
      - Product and design software
      - Platform and storage solutions
      - Operations software
      - Operations management tools
      - Marketing technologies
      - IT security solutions
      - IT management systems
      - HR software
      - Health tech applications
      - Finance and accounting tools
      - E-commerce platforms
      - DevOps and development tools
      - Customer management systems
      - Computer networks
      - Communications tools
      - Collaboration platforms
      - Business intelligence and analytics

    """
    return make_api_request(
        "businesses/technographics/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_company_ratings(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get internal company ratings in bulk.
    Returns:
    - Employee satisfaction ratings across multiple categories
    - Company culture and work-life balance assessments
    - Management and leadership quality ratings
    - Career growth and advancement opportunities metrics
    - Interview experience feedback from candidates
    - Overall company reputation scores from current and former employees
    """
    return make_api_request(
        "businesses/company_ratings_by_employees/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_financial_metrics(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field(),
    date: str | None = Field(
        default=None, description="Optional ISO 8601 timestamp for financial metrics"
    ),
):
    """
    Get financial metrics for public companies in bulk.
    Returns:
    - Financial metrics including EBITDA, revenue, and cost of goods sold (COGS)
    - Profitability indicators like ROA (Return on Assets) and ROC (Return on Capital)
    - Asset turnover and working capital figures
    - Price-to-earnings ratio and enterprise value metrics
    - Executive leadership details including names, titles, and compensation
    - Earnings surprises with actual vs. estimated results
    - Peer companies for competitive analysis
    - Total shareholder return (TSR) metrics for various time periods

    """
    payload = {"business_ids": business_ids}
    if date:
        payload["parameters"] = {"date": date}

    return make_api_request("businesses/financial_indicators/bulk_enrich", payload)


@mcp.tool()
def enrich_businesses_funding_and_acquisitions(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get businesses funding and acquisition history in bulk.
    Returns:
    - Detailed funding history including dates, amounts, and round types
    - IPO information including date and size
    - List of investors and lead investors for each funding round
    - Total known funding value
    - Current board members and advisors
    - Acquisition information (if applicable)
    - First and latest funding round details
    - Number of funding rounds and investors
    """
    return make_api_request(
        "businesses/funding_and_acquisition/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_challenges(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get insights on the challenges, breaches, and competition of public companies.
    Returns:
    - Technological disruption challenges identified in SEC filings
    - Data security breaches and cybersecurity vulnerabilities
    - Market saturation concerns and competitive pressures
    - Data security and privacy regulatory compliance issues
    - Competitive landscape and market position challenges
    - Customer adoption risks and third-party dependencies
    - Links to official SEC filings and documents
    - Company identifiers including ticker symbols and CIK numbers
    - Filing dates and form types for regulatory submissions
    """
    return make_api_request(
        "businesses/pc_business_challenges_10k/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_competitive_landscape(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get insights on the market landscape of public companies.
    Returns:
    - Competitive differentiation strategies from SEC filings
    - Key competitors identified in public disclosures
    - Company ticker symbols and CIK identifiers
    - Links to official SEC filings and documents
    - Filing dates and form types for regulatory submissions
    """
    return make_api_request(
        "businesses/pc_competitive_landscape_10k/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_strategic_insights(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get strategic insights for public companies.
    Returns:
    - Strategic focus areas and company value propositions from SEC filings
    - Target market segments and customer demographics
    - Product development roadmaps and innovation initiatives
    - Marketing and sales strategies from public disclosures
    - Strategic partnerships and acquisition information
    - Company identifiers including ticker symbols and CIK numbers
    - Links to official SEC filings and documents
    - Filing dates and form types for regulatory submissions
    """
    return make_api_request(
        "businesses/pc_strategy_10k/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_workforce_trends(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get workforce trends and department composition for companies.
    Returns:
    - Percentage breakdown of employees across different departments (engineering, sales, marketing, etc.)
    - Changes in department composition compared to previous quarter
    - Total employee profiles found per quarter
    - Quarterly timestamp information for trend analysis
    - Insights into company structure and hiring priorities
    - Department growth or reduction indicators
    """
    return make_api_request(
        "businesses/workforce_trends/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_linkedin_posts(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field()
):
    """
    Get LinkedIn posts for public companies.
    Returns:
    - Post text content from company LinkedIn posts
    - Post URLs for direct access to original content
    - Engagement metrics including number of likes and comments
    - Publication dates and time since posting
    - Company display names when available
    - Historical social media content for trend analysis
    - Marketing messaging and brand voice examples
    - Product announcements and company updates
    """
    return make_api_request(
        "businesses/linkedin_posts/bulk_enrich",
        {"business_ids": business_ids},
    )


@mcp.tool()
def enrich_businesses_website_changes(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field(),
    keywords: List[str] | None = Field(
        default=None,
        description="List of keywords to search for in website changes",
    ),
):
    """
    Get website changes for public companies.
    Returns:
    - Website content changes with before and after text comparisons
    - Strategic implications of content modifications
    - Dates when changes were detected
    - Changes in featured products, services, or content
    - Shifts in marketing messaging or positioning
    - Updates to promotional content and featured items
    - Changes in top charts or featured content listings
    - Insights into business strategy and market focus
    """
    payload = {"business_ids": business_ids}
    if keywords:
        payload["parameters"] = {"keywords": keywords}
    return make_api_request(
        "businesses/website_changes/bulk_enrich",
        payload,
    )


@mcp.tool()
def enrich_businesses_website_keywords(
    business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field(),
    keywords: List[str] | None = Field(
        default=None,
        description="List of keywords to search for in website keywords",
    ),
):
    """
    Get website keywords for public companies.
    For each keyword, input multiple search terms separated by commas (","), which simulates a logical "AND" operation.
    Returns:
    - Website URL
    - Keywords indicator showing if keywords were found
    - Text results containing:
        - Position/rank of the result
        - Text snippet showing keyword matches
        - URL where the keyword was found
    """
    payload = {"business_ids": business_ids}
    if keywords:
        payload["parameters"] = {"keywords": keywords}
    return make_api_request(
        "businesses/company_website_keywords/bulk_enrich",
        payload,
    )
