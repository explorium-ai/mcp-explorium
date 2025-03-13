import src.explorium_mcp_server.mcp_server_research as mcp_server_research

session_id = mcp_server_research.create_research_session(
    {
        "linkedin_category": [
            "software development",
            "desktop computing software products",
            "mobile computing software products",
        ],
        "region_country_code": ["us-ca"],
        "company_size": ["1-10", "11-50", "51-200", "201-500"],
    }
)["session_id"]

result = mcp_server_research.session_load_more_results(session_id)
mcp_server_research.session_enrich(
    session_id, enrichment_types=["company_ratings", "firmographics"]
)
print(result)
