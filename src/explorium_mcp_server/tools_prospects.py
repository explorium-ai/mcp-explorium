from . import _shared
from ._shared import (
    mcp,
    make_api_request,
    get_filters_payload,
    enum_list_to_serializable,
)
from pydantic import conlist, Field
from typing import List
from . import models
from functools import partial

prospect_ids_field = partial(
    Field, description="List of up to 50 Explorium prospect IDs from match_prospects"
)


@mcp.tool()
def match_prospects(
    prospects_to_match: conlist(
        models.prospects.ProspectMatchInput, min_length=1, max_length=40
    )
):
    """
    Get the Explorium prospect ID from a prospect's email, full name, and company.
    At least email OR (full name AND company) must be provided.

    Use this when:
    - Need prospect enrichment tools
    - Getting a prospect's contact information
    - Analyzing an individual's social media presence
    - Gathering information on a person's professional profile and workplace
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
        default=100, le=1000, description="The number of prospects to return"
    ),
    page_size: int = Field(
        default=100, le=100, description="The number of prospects to return per page"
    ),
    page: int = Field(default=1, description="The page number to return"),
):
    """
    Get a list of prospects according to filters such as job level, department, or other professional attributes.
    If looking for prospects from a specific business, use the business_id filter.

    Use this when:
    - Performing sales intelligence research
    - Identifying high-value prospects
    - Enacting prospecting workflows

    This tool returns Prospect IDs, which can be used to fetch more information.
    Do NOT call match_prospects afterwards if the response already contains
    prospect IDs.
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

    return make_api_request("prospects/events", payload)


# Enrichment tools


@mcp.tool()
def enrich_prospects_contacts_information(
    prospect_ids: conlist(str, min_length=1, max_length=50) = prospect_ids_field()
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
    prospect_ids: conlist(str, min_length=1, max_length=50) = prospect_ids_field()
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
    prospect_ids: conlist(str, min_length=1, max_length=50) = prospect_ids_field()
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
