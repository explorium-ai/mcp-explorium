import asyncio
import shortuuid
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Literal
from ._shared import pydantic_model_to_serializable
from pydantic import Field, BaseModel

from . import tools_businesses
from . import models

import inspect
import time
from datetime import datetime, timedelta

# At the top of your tools_businesses.py file
ENRICHMENT_TOOLS = {
    "firmographics": tools_businesses.enrich_businesses_firmographics,
    "technographics": tools_businesses.enrich_businesses_technographics,
    "company_ratings": tools_businesses.enrich_businesses_company_ratings,
    "financial_metrics": tools_businesses.enrich_businesses_financial_metrics,
    "funding_and_acquisitions": tools_businesses.enrich_businesses_funding_and_acquisitions,
    "challenges": tools_businesses.enrich_businesses_challenges,
    "competitive_landscape": tools_businesses.enrich_businesses_competitive_landscape,
    "strategic_insights": tools_businesses.enrich_businesses_strategic_insights,
    "workforce_trends": tools_businesses.enrich_businesses_workforce_trends,
    "linkedin_posts": tools_businesses.enrich_businesses_linkedin_posts,
    "website_changes": tools_businesses.enrich_businesses_website_changes,
    "website_keywords": tools_businesses.enrich_businesses_website_keywords,
}

ENRICHMENT_DOCS: Dict[str, str] = {
    name: inspect.getdoc(func) for name, func in ENRICHMENT_TOOLS.items()
}

EnrichmentType = Literal[
    "firmographics",
    "technographics",
    "company_ratings",
    "financial_metrics",
    "funding_and_acquisitions",
    "challenges",
    "competitive_landscape",
    "strategic_insights",
    "workforce_trends",
    "linkedin_posts",
    "website_changes",
    "website_keywords",
]
# Create a FastMCP server for the agent layer
research_mcp = FastMCP("research_mcp", dependencies=["requests", "dotenv", "pydantic"])


class ResearchResultsPage(BaseModel):
    items: List[models.businesses.Business]
    page_index: int


class ResearchSessionResult(BaseModel):
    business_id: str
    data: Any | None = None
    enrichments: Dict[EnrichmentType, Any] = {}


class ResearchSession:
    def __init__(
        self,
        filters: models.businesses.FetchBusinessesFilters | None = None,
        max_results: int | None = None,
    ):
        self.session_id = shortuuid.ShortUUID().random(length=8)
        self.filters = filters
        self.max_results = max_results
        self.results: Dict[str, ResearchSessionResult] = {}
        self.current_page_index: int = 0
        self.total_pages: int | None = None
        self.total_results: int | None = None
        self.last_modified = time.time()

    def get_total_loaded_results(self) -> int:
        """The total number of results that have been loaded."""
        return len(self.results)

    def get_is_started(self) -> bool:
        """Whether the research session has started."""
        return self.total_results is not None

    def load_more_results(self):
        """Load more results from the API."""
        # if (
        #     self.total_results is not None
        #     and self.get_total_loaded_results() >= self.total_results
        # ):
        #     raise ValueError("No more results to load for this session.")

        is_first_page = self.current_page_index == 0
        next_page_index = self.current_page_index + 1
        response = tools_businesses.fetch_businesses(
            self.filters, page=next_page_index, size=self.max_results
        )
        if not response["data"]:
            return
        for business in response["data"]:
            result = ResearchSessionResult(
                business_id=business["business_id"], data=business, enrichments={}
            )
            self.results[business["business_id"]] = result
        self.current_page_index = next_page_index

        # If this was the first page, set properties
        if is_first_page:
            self.total_pages = response["total_pages"]
            self.total_results = response["total_results"]

    def touch(self):
        """Update the last modified timestamp"""
        self.last_modified = time.time()

    def is_expired(self, ttl_hours: int = 1) -> bool:
        """Check if session has expired based on TTL"""
        return (time.time() - self.last_modified) > (ttl_hours * 3600)


import os
import json

research_sessions: Dict[str, ResearchSession] = {}


def save_sessions():
    serializable_sessions = {}
    for session_id, session in research_sessions.items():
        serializable_sessions[session_id] = {
            "session_id": session.session_id,
            "filters": pydantic_model_to_serializable(session.filters),
            "max_results": session.max_results,
            "results": {
                bid: {
                    "business_id": result.business_id,
                    "data": pydantic_model_to_serializable(result.data),
                    "enrichments": result.enrichments,
                }
                for bid, result in session.results.items()
            },
            "current_page_index": session.current_page_index,
            "total_pages": session.total_pages,
            "total_results": session.total_results,
            "last_modified": session.last_modified,
        }

    with open("research_sessions.json", "w") as f:
        json.dump(serializable_sessions, f)


def load_sessions():
    if os.path.exists("research_sessions.json"):
        with open("research_sessions.json", "r") as f:
            loaded_sessions = json.loads(f.read())
            for session_id, session_data in loaded_sessions.items():
                # Create a new session with the basic attributes
                session = ResearchSession(
                    filters=(
                        models.businesses.FetchBusinessesFilters(
                            **session_data["filters"]
                        )
                        if session_data["filters"]
                        else {}
                    ),
                    max_results=session_data["max_results"],
                )
                # Restore other attributes
                session.session_id = session_data["session_id"]
                session.current_page_index = session_data["current_page_index"]
                session.total_pages = session_data["total_pages"]
                session.total_results = session_data["total_results"]
                session.last_modified = session_data.get("last_modified", time.time())

                # Restore results
                for bid, result_data in session_data["results"].items():
                    session.results[bid] = ResearchSessionResult(
                        business_id=result_data["business_id"],
                        data=result_data["data"],
                        enrichments=result_data["enrichments"],
                    )

                # Only load non-expired sessions
                if not session.is_expired():
                    research_sessions[session_id] = session


def cleanup_expired_sessions(ttl_hours: int = 24):
    """Remove expired sessions"""
    expired = [
        sid
        for sid, session in research_sessions.items()
        if session.is_expired(ttl_hours)
    ]
    for sid in expired:
        del research_sessions[sid]
    if expired:
        save_sessions()
    return len(expired)


research_mcp.add_tool(tools_businesses.autocomplete)

SAMPLE_MAX_RESULTS = 2


def return_sample_data(session_id: str):
    session = research_sessions[session_id]
    sample_data = []
    for business_id in session.results:
        sample_data.append(session.results[business_id].data)
        if len(sample_data) >= SAMPLE_MAX_RESULTS:
            break
    return sample_data


@research_mcp.tool()
def create_search_session(
    filters: models.businesses.FetchBusinessesFilters,
    max_results: int = 10,
):
    """
    Start a new research session for businesses for the given filters.
    Do not use this tool if no filters are provided.
    Do not create more than one research session at a time.
    You MUST call the autocomplete tool to get the list of possible values for
    filters specified in the autocomplete tool's description.

    Do NOT use this tool first if you do not have a list of available values for
    mandatory filters specified in the autocomplete tool's description.

    Do not send empty values/lists for filters.

    Returns the session ID, which can be used to load more results.
    The data is not returned to save tokens. Use session_view_data to get the final results.

    IMPORTANT: HOW TO USE THIS TOOL:
    - Use the autocomplete tool to create a single research session.
    - Use session_enrich to enrich the businesses in the session.
    - Use session_view_data to get the final results. Only use this tool once you have finished enriching.
    """
    session = ResearchSession(filters, max_results)
    research_sessions[session.session_id] = session
    session_load_more_results(session.session_id)
    save_sessions()
    return {
        "session_id": session.session_id,
        "session_details": get_session_details(session.session_id),
        "sample_data": return_sample_data(session.session_id),
    }


@research_mcp.tool()
def create_company_research_session(
    company_inputs: List[models.businesses.MatchBusinessInput],
):
    """
    Create a research session for SPECIFIC companies.
    It is recommended to fetch firmographics after creating the session.
    company_inputs (List[models.businesses.MatchBusinessInput]): A list of company inputs to research.
    """
    session = ResearchSession(filters=None, max_results=1)
    results = tools_businesses.match_businesses(company_inputs)
    if results["total_matches"] == 0:
        return {"error": "No companies found"}
    for result in results["matched_businesses"]:
        session.results[result["business_id"]] = ResearchSessionResult(
            business_id=result["business_id"],
            data=result,
            enrichments={},
        )
    research_sessions[session.session_id] = session
    save_sessions()
    return {
        "session_id": session.session_id,
        "session_details": get_session_details(session.session_id),
        "sample_data": return_sample_data(session.session_id),
    }


@research_mcp.tool()
def get_session_details(session_id: str | None = None):
    """
    Get the details of a research session.
    session_id (str | None): The ID of the research session to get details for. If not provided, all sessions will be returned.
    """
    if session_id is None:
        return [
            {
                "session_id": session.session_id,
                "filters": pydantic_model_to_serializable(session.filters),
            }
            for session in research_sessions.values()
        ]
    else:
        if session_id not in research_sessions:
            return {"error": f"Session {session_id} not found"}
        session = research_sessions[session_id]
        return {
            "session_id": session.session_id,
            "filters": pydantic_model_to_serializable(session.filters),
            "total_results": session.total_results,
            "total_pages": session.total_pages,
        }


@research_mcp.tool()
def session_load_more_results(session_id: str):
    """
    Load the next page of businesses for the given research session.
    session_id (str): The ID of the research session to load more results for.
    """
    if session_id not in research_sessions:
        return {"error": f"Session {session_id} not found"}
    session = research_sessions[session_id]
    num_loaded_before = session.get_total_loaded_results()
    session.load_more_results()
    session.touch()
    num_loaded_after = session.get_total_loaded_results()
    session_details = get_session_details(session_id)

    if num_loaded_after - num_loaded_before > 0:
        save_sessions()

    return {
        "message": f"Loaded {num_loaded_after - num_loaded_before} results for session {session_id}.",
        "session_details": session_details,
    }


@research_mcp.tool()
def session_view_data(session_id: str):
    """
    Get the final results of a research session.
    This will return the results of the research session as a list of business objects.
    Do NOT use this tool until the end of your research session.
    session_id (str): The ID of the research session to get results for.
    """
    if session_id not in research_sessions:
        return {"error": f"Session {session_id} not found"}
    session = research_sessions[session_id]
    results = session.results
    return pydantic_model_to_serializable(results)


# Format the docstring with enrichment documentation
def _format_enrichment_docs() -> str:
    docs = []
    for name, doc in ENRICHMENT_DOCS.items():
        docs.append(f"\n--- {name} ---\n{doc}")

    return "\n".join(docs)


@research_mcp.tool()
def get_business_id(session_id: str, name: str, domain: str):
    """
    Get the business ID for a given name and domain.
    Only returns results for the given session.
    """
    if session_id not in research_sessions:
        return {"error": f"Session {session_id} not found"}
    session = research_sessions[session_id]
    for business_id, result in session.results.items():
        if result.data["name"] == name and result.data["domain"] == domain:
            return business_id
    return None


MAX_BUSINESSES_PER_ENRICH_CALL = 50


@research_mcp.tool()
def session_enrich(
    session_id: str,
    enrichment_types: List[EnrichmentType] = Field(
        description="The types of enrichment to perform.", min_length=1, max_length=5
    ),
):
    """
    Enrich the businesses in the given research session.

    Available enrichment types:
    {enrichment_docs}
    """
    if session_id not in research_sessions:
        return {"error": f"Session {session_id} not found"}
    session = research_sessions[session_id]
    session.touch()
    business_ids = list(session.results.keys())

    # Split the business IDs into chunks of MAX_BUSINESSES_PER_ENRICH_CALL
    business_id_chunks = [
        business_ids[i : i + MAX_BUSINESSES_PER_ENRICH_CALL]
        for i in range(0, len(business_ids), MAX_BUSINESSES_PER_ENRICH_CALL)
    ]

    print(f"Enriching {len(business_id_chunks)} chunk(s)")

    success_samples = []

    # Parallelize the enrichment calls of each chunk, printing the progress
    for chunk_index, chunk in enumerate(business_id_chunks):
        print(f"Enriching chunk {chunk_index + 1} of {len(business_id_chunks)}")
        for enrichment_type in enrichment_types:
            print(f"Enriching {enrichment_type} ({len(chunk)} items)")
            results = ENRICHMENT_TOOLS[enrichment_type](chunk)
            if not results or "data" not in results or results["data"] is None:
                for business_id in chunk:
                    session.results[business_id].enrichments[enrichment_type] = {
                        "info": f"No {enrichment_type} results found"
                    }
            else:
                found_business_ids = []
                for result in results["data"]:
                    if result["data"]:
                        session.results[result["business_id"]].enrichments[
                            enrichment_type
                        ] = result["data"]
                        found_business_ids.append(result["business_id"])
                        success_samples.append(result["data"])
                # Partial enrichment results - add no results found for the missing businesses
                for business_id in [
                    business_id
                    for business_id in chunk
                    if business_id not in found_business_ids
                ]:
                    session.results[business_id].enrichments[enrichment_type] = {
                        "info": f"No {enrichment_type} results found"
                    }

    # Return a sample of the data to see what was found
    if success_samples:
        save_sessions()
        return {"info": "Successfully enriched businesses."}
    else:
        return {"info": "All enrichments returned no results."}


# Update the session_enrich docstring with the formatted documentation
session_enrich.__doc__ = session_enrich.__doc__.format(
    enrichment_docs=_format_enrichment_docs()
)

load_sessions()
cleanup_expired_sessions()
# Run the agent server
if __name__ == "__main__":
    asyncio.run(research_mcp.run())
