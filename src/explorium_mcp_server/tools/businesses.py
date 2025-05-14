from functools import partial
from typing import List, Dict, Any, Union, Optional

from pydantic import conlist, Field

from explorium_mcp_server import models
from explorium_mcp_server.tools.shared import (
    mcp,
    make_api_request,
    enum_list_to_serializable,
    pydantic_model_to_serializable,
    get_filters_payload,
    create_session,
    get_session_data,
    save_session_data,
)
from explorium_mcp_server.models.enum_types import AutocompleteType

business_ids_field = partial(
    Field, description="List of Explorium business IDs from match_businesses"
)


@mcp.tool()
def match_businesses(
        businesses_to_match: conlist(
            models.businesses.MatchBusinessInput, min_length=1, max_length=50
        ),
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
):
    """
    Get the Explorium business IDs from business name and/or domain in bulk.
    Use this when:
    - Need company size/revenue/industry
    - Analyzing overall business metrics
    - Researching company background
    - Looking for specific employees (use fetch_prospects next)

    Do NOT use when:
    - Looking for specific employees
    - Getting executive contact info
    - Finding team member details
    - You already called fetch_businesses - the response already contains business IDs
    
    Returns session_id in the response which can be used for future data retrieval.
    """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the input in the session
    save_session_data(session_id, "businesses_to_match", businesses_to_match)
    
    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses/match",
        {"businesses_to_match": businesses_to_match},
        session_id=session_id,
        session_key="match_businesses_result"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result


@mcp.tool()
def fetch_businesses(
        filters: models.businesses.FetchBusinessesFilters,
        size: int = Field(
            default=1000, le=1000, description="The number of businesses to return"
        ),
        page_size: int = Field(
            default=5, le=100, description="The number of businesses to return per page - recommended: 5"
        ),
        page: int = Field(default=1, description="The page number to return"),
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
):
    """
     Fetch businesses from the Explorium API using filter criteria.

     USAGE WITH SESSION:
     - If you provide a session_id, the filters and results will be stored for future reference
     - If not provided, a new session_id will be created and returned in the response
     - Use the session_id to retrieve stored data with get_session_businesses

     For filters backed by enums in the schema, use the enum values directly:
     - `company_revenue`
     - `company_age`
     - `company_size`
     - `number_of_locations`

     For the following filters, you MUST first call the `autocomplete` tool to retrieve valid values:
     - `linkedin_category`
     - `company_tech_stack_categories`
     - `job_title`
     - `google_category`
     - `naics_category`
     - `country_code`
     - `region_country_code`
     - `company_tech_stack_category`
     - `company_tech_stack_tech`
     - `company_name`
     - `city_region_country`

     Do NOT use this tool until all required autocomplete values have been retrieved.

     Rules:
     - Only one of `linkedin_category`, `google_category`, or `naics_category` can be set per request.
     - This tool returns Business IDs. Do NOT follow with `match_businesses`.
     - To get employee data for companies, use `fetch_prospects`.
     - If any filter is invalid or unsupported, stop and alert the user.
     """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the filters in the session
    save_session_data(session_id, "fetch_businesses_filters", filters)
    save_session_data(session_id, "fetch_businesses_params", {
        "size": size,
        "page_size": page_size,
        "page": page
    })
    
    payload = {
        "mode": "full",
        "size": size,
        "page_size": min(
            pydantic_model_to_serializable(page_size),
            pydantic_model_to_serializable(size),
        ),
        "page": page,
        "filters": get_filters_payload(filters),
        "request_context": {},
    }

    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses", 
        payload,
        session_id=session_id,
        session_key="fetch_businesses_result"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result


@mcp.tool()
def autocomplete(
        field: AutocompleteType,
        query: Union[str, int] = Field(description="The query to autocomplete"),
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
):
    """
    Autocomplete values for business filters based on a query.
    Never use for fields not explicitly listed (e.g., `website_keywords`).
    Prefer `linkedin_category` over `google_category` when both apply.
    Always call autocomplete requests in **parallel**, not sequentially.

    Hints:
    - Searching for SaaS? Use the keyword 'software'
    - Use 'country' to retrieve ISO codes
    
    Returns session_id in the response which can be used for future data retrieval.
    """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the autocomplete parameters
    save_session_data(session_id, f"autocomplete_{field}_{query}", {
        "field": field,
        "query": query
    })
    
    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses/autocomplete", 
        method="GET", 
        params={"field": field, "query": query},
        session_id=session_id,
        session_key=f"autocomplete_result_{field}_{query}"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result


@mcp.tool()
def get_session_businesses(
        session_id: str = Field(description="Session ID to retrieve data from"),
        key: str = Field(description="Key of the stored data to retrieve")
):
    """
    Retrieve previously stored business data from a session.
    
    This tool allows you to access data that was stored in previous API calls
    without having to pass large datasets between function calls.
    
    Args:
        session_id: The session identifier from a previous API call
        key: The specific key to retrieve (e.g., "fetch_businesses_result", "match_businesses_result")
    """
    data = get_session_data(session_id, key)
    
    if data is None:
        available_keys = get_session_data(session_id, "__keys__") or []
        if not available_keys:
            # Try to get all keys for the session
            from explorium_mcp_server.storage.session import list_session_keys
            available_keys = list_session_keys(session_id)
            
        return {
            "error": f"No data found for session {session_id} with key {key}",
            "available_keys": available_keys,
            "session_id": session_id
        }
        
    return {
        "session_id": session_id,
        "key": key,
        "data": data
    }


@mcp.tool()
def fetch_businesses_events(
        business_ids: conlist(str, min_length=1, max_length=20) = business_ids_field(),
        event_types: List[models.businesses.BusinessEventType] = Field(
            description="List of event types to fetch"
        ),
        timestamp_from: str = Field(description="ISO 8601 timestamp"),
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
) -> Dict[str, Any]:
    """
    Retrieves business-related events from the Explorium API in bulk.
    If you're looking for events related to role changes, you should use the
    prospects events tool instead.

    This is a VERY useful tool for researching a company's events and history.
    
    Returns session_id in the response which can be used for future data retrieval.
    """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the parameters in the session
    save_session_data(session_id, "fetch_businesses_events_params", {
        "business_ids": business_ids,
        "event_types": [str(event_type) for event_type in event_types],
        "timestamp_from": timestamp_from
    })
    
    payload = {
        "business_ids": business_ids,
        "event_types": enum_list_to_serializable(event_types),
        "timestamp_from": timestamp_from,
    }

    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses/events", 
        payload, 
        timeout=120,
        session_id=session_id,
        session_key="fetch_businesses_events_result"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result


@mcp.tool()
def fetch_businesses_statistics(
        filters: models.businesses.FetchBusinessesFilters,
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
):
    """
    Fetch aggregated insights into businesses by industry, revenue, employee count, and geographic distribution.
    
    Returns session_id in the response which can be used for future data retrieval.
    """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the filters in the session
    save_session_data(session_id, "fetch_businesses_statistics_filters", filters)
    
    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses/stats",
        {"filters": get_filters_payload(filters)},
        session_id=session_id,
        session_key="fetch_businesses_statistics_result"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result


# Enrichment tools


@mcp.tool()
def enrich_businesses_firmographics(
        business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field(),
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
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

    **Do NOT use when**:
    - You need to find a specific employee at a company
    - Looking for leadership info of a company
    
    Returns session_id in the response which can be used for future data retrieval.
    """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the business IDs in the session
    save_session_data(session_id, "enrich_businesses_firmographics_ids", business_ids)
    
    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses/firmographics/bulk_enrich",
        {"business_ids": business_ids},
        session_id=session_id,
        session_key="enrich_businesses_firmographics_result"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result


@mcp.tool()
def enrich_businesses_technographics(
        business_ids: conlist(str, min_length=1, max_length=50) = business_ids_field(),
        session_id: Optional[str] = Field(default=None, description="Session ID for storing results")
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
      
    Returns session_id in the response which can be used for future data retrieval.
    """
    # Create a new session if none provided
    if not session_id:
        session_id = create_session()
    
    # Store the business IDs in the session
    save_session_data(session_id, "enrich_businesses_technographics_ids", business_ids)
    
    # Make the API request and store the result in the session
    result = make_api_request(
        "businesses/technographics/bulk_enrich",
        {"business_ids": business_ids},
        session_id=session_id,
        session_key="enrich_businesses_technographics_result"
    )
    
    # Include the session_id in the response
    result["session_id"] = session_id
    
    return result

# ... Add session support for remaining enrichment tools
