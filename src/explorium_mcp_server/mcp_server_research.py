import asyncio
import uuid
import requests
from mcp.server.fastmcp import FastMCP, Context
from mcp.server import Server
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.mcp.mcp_aggregator import MCPAggregator
from typing import List, Dict, Any, Optional, Literal
from concurrent.futures import ThreadPoolExecutor
from ._shared import BASE_URL, EXPLORIUM_API_KEY, pydantic_model_to_serializable
from pydantic import Field, BaseModel
from dataclasses import dataclass

from . import tools_businesses
from . import models

import inspect

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

EnrichmentType = Literal[tuple(ENRICHMENT_TOOLS.keys())]
# Create a FastMCP server for the agent layer
research_mcp = FastMCP(
    "research_mcp", dependencies=["mcp_agent", "requests", "dotenv", "pydantic"]
)


class ResearchResultsPage(BaseModel):
    items: List[models.businesses.Business]
    page_index: int


class ResearchSessionResult(BaseModel):
    business_id: str
    data: models.businesses.Business
    enrichments: Dict[EnrichmentType, Any]


class ResearchSession:
    def __init__(
        self,
        filters: models.businesses.FetchBusinessesFilters,
        max_results: int | None = None,
    ):
        self.session_id = str(uuid.uuid4())
        self.filters = filters
        self.max_results = max_results
        self.results: Dict[str, ResearchSessionResult] = {}
        self.current_page_index: int = 0
        self.total_pages: int | None = None
        self.total_results: int | None = None

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


research_sessions: Dict[str, ResearchSession] = {}


class AutocompleteInput(BaseModel):
    field: Literal[
        "country",
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
    ]
    query: str | int = Field(description="The query to autocomplete")


research_mcp.add_tool(tools_businesses.autocomplete)


@research_mcp.tool()
def create_research_session(
    filters: models.businesses.FetchBusinessesFilters,
    max_results: int = 10,
):
    """
    Start a new research session for businesses for the given filters.
    Do not use this tool if no filters are provided.
    You MUST call the autocomplete tool to get the list of possible values for
    filters specified in the autocomplete tool's description.

    Do NOT use this tool first if you do not have a list of available values for
    mandatory filters specified in the autocomplete tool's description.

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
    return {
        "session_id": session.session_id,
        "session_details": get_session_details(session.session_id),
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
    session = research_sessions[session_id]
    num_loaded_before = session.get_total_loaded_results()
    num_loaded = session.load_more_results()
    num_loaded_after = session.get_total_loaded_results()
    session_details = get_session_details(session_id)
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
    session = research_sessions[session_id]
    results = session.results
    return pydantic_model_to_serializable(results)


# Format the docstring with enrichment documentation
def _format_enrichment_docs() -> str:
    docs = []
    for name, doc in ENRICHMENT_DOCS.items():
        # Extract the "Returns:" section from the docstring
        # returns_section = ""
        # if "Returns:" in doc:
        #     returns_section = doc.split("Returns:")[1].split("Do NOT use")[0].strip()

        # Format the documentation
        docs.append(f"\n--- {name} ---\n{doc}")

    return "\n".join(docs)


@research_mcp.tool()
def get_business_id(session_id: str, name: str, domain: str):
    """
    Get the business ID for a given name and domain.
    Only returns results for the given session.
    """
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
    session = research_sessions[session_id]
    # business_ids = (
    #     list(session.results.keys())
    #     if business_ids_to_enrich is None
    #     else business_ids_to_enrich
    # )
    business_ids = list(session.results.keys())

    # Split the business IDs into chunks of MAX_BUSINESSES_PER_ENRICH_CALL
    business_id_chunks = [
        business_ids[i : i + MAX_BUSINESSES_PER_ENRICH_CALL]
        for i in range(0, len(business_ids), MAX_BUSINESSES_PER_ENRICH_CALL)
    ]

    print(
        f"Enriching {len(business_id_chunks)} chunks of {MAX_BUSINESSES_PER_ENRICH_CALL} businesses each..."
    )

    # Parallelize the enrichment calls of each chunk, printing the progress
    for chunk_index, chunk in enumerate(business_id_chunks):
        print(f"Enriching chunk {chunk_index + 1} of {len(business_id_chunks)}...")
        for enrichment_type in enrichment_types:
            print(f"Enriching {enrichment_type} for {len(chunk)} businesses...")
            results = ENRICHMENT_TOOLS[enrichment_type](chunk)
            if results["data"] is None:
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
                # Partial enrichment results - add no results found for the missing businesses
                for business_id in [
                    business_id
                    for business_id in chunk
                    if business_id not in found_business_ids
                ]:
                    session.results[business_id].enrichments[enrichment_type] = {
                        "info": f"No {enrichment_type} results found"
                    }

    print("Enrichment(s) complete.")


# Update the session_enrich docstring with the formatted documentation
session_enrich.__doc__ = session_enrich.__doc__.format(
    enrichment_docs=_format_enrichment_docs()
)

# Run the agent server
if __name__ == "__main__":
    asyncio.run(research_mcp.run())
