from functools import partial
from typing import List

from pydantic import conlist, Field

from explorium_mcp_server import models
from explorium_mcp_server.tools.shared import (
    mcp,
    make_api_request,
    get_filters_payload,
    enum_list_to_serializable,
)

prospect_ids_field = partial(
    Field, description="List of up to 50 Explorium prospect IDs from match_prospects"
)


@mcp.tool()
def match_prospects(
        prospects_to_match: conlist(
            models.prospects.ProspectMatchInput, min_length=1, max_length=40
        ),
):
    """
    Get the Explorium prospect ID from a prospect's email, full name, and company.
    At least email OR (full name AND company) must be provided.
    You MUST use this tool if the input is about someone working at a specific company.

    Use this when:
    - Need prospect enrichment tools
    - Getting contact information
    - Analyzing an individual's social media presence
    - Gathering information on a person's professional profile and workplace

    Do NOT use for:
    - Finding leadership information (CEO, CTO, CFO, etc.)
    - Looking for employees at a company
    """
    for prospect_to_match in prospects_to_match:
        if not prospect_to_match.email and (
                not prospect_to_match.full_name or not prospect_to_match.company_name
        ):
            raise ValueError(
                "Either email OR (full name AND company) must be provided."
            )
    return make_api_request(
        "prospects/match",
        {"prospects_to_match": prospects_to_match},
    )


@mcp.tool()
def fetch_prospects(
        filters: models.prospects.FetchProspectsFilters,
        size: int = Field(
            default=1000, le=1000, description="The number of prospects to return"
        ),
        page_size: int = Field(
            default=5,
            le=100,
            description="The number of prospects to return per page - recommended: 5",
        ),
        page: int = Field(default=1, description="The page number to return"),
):
    """
    Fetch prospects (employees) using filters such as job level, department, and other professional attributes.

    You MUST use the autocomplete tool to retrieve valid values for required filters before calling this tool.

    Do NOT call this tool first if you don’t have the necessary filter values.

    Returns Prospect IDs for individuals at specific companies.

    If a requested filter is not supported by the Explorium API, stop execution and inform the user.

    Use fetch_businesses if you're looking for companies instead.

    For leadership details at public companies, use enrich_businesses_financial_metrics.
    """

    data = {
        "mode": "full",
        "size": size,
        "page_size": page_size,
        "page": page,
        "filters": get_filters_payload(filters),
    }

    return make_api_request("prospects", data)


@mcp.tool()
def fetch_prospects_events(
        prospect_ids: conlist(str, min_length=1, max_length=20) = prospect_ids_field(),
        event_types: List[models.prospects.ProspectEventType] = Field(
            description="List of event types to fetch"
        ),
        timestamp_from: str = Field(description="ISO 8601 timestamp"),
):
    """
    Retrieves prospect-related events from the Explorium API in bulk.
    Use this when querying for prospect-related events about businesses:
    Example workflow:
    Fetch businesses > Fetch prospects > Fetch prospects events
    """
    payload = {
        "prospect_ids": prospect_ids,
        "event_types": enum_list_to_serializable(event_types),
        "timestamp_from": timestamp_from,
    }

    return make_api_request("prospects/events", payload, timeout=120)


# Enrichment tools


@mcp.tool()
def enrich_prospects_contacts_information(
        prospect_ids: conlist(str, min_length=1, max_length=50) = prospect_ids_field(),
):
    """
    Enrich prospect contact information with additional details.
    Returns:
    - Professional and personal email addresses
    - Email type (professional/personal)
    - Phone numbers
    """
    return make_api_request(
        "prospects/contacts_information/bulk_enrich", {"prospect_ids": prospect_ids}
    )


@mcp.tool()
def enrich_prospects_linkedin_posts(
        prospect_ids: conlist(str, min_length=1, max_length=50) = prospect_ids_field(),
):
    """
    Enrich prospect LinkedIn posts with additional details.
    Returns:
    - Post text content
    - Post engagement metrics (likes, comments)
    - Post URLs
    - Post creation dates
    - Days since posted
    """
    return make_api_request(
        "prospects/linkedin_posts/bulk_enrich", {"prospect_ids": prospect_ids}
    )


@mcp.tool()
def enrich_prospects_profiles(
        prospect_ids: conlist(str, min_length=1, max_length=50) = prospect_ids_field(),
):
    """
    Get detailed profile information for prospects.
    Returns:
    - Full name and demographic details (age group, gender)
    - Location information (country, region, city)
    - LinkedIn profile URL
    - Current role details:
      - Company name and website
      - Job title, department and seniority level
    - Work experience history:
      - Company names and websites
      - Job titles with role classifications
      - Start/end dates
      - Primary role indicator
    - Education background:
      - Schools attended with dates
      - Degrees, majors and minors
    - Skills and interests when available
    """
    return make_api_request(
        "prospects/profiles/bulk_enrich", {"prospect_ids": prospect_ids}
    )
