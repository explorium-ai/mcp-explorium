import src.explorium_mcp_server.mcp_server_research as mcp_server_research

session_id = mcp_server_research.create_research_session(
    {
        "linkedin_category": ["software development", "healthcare"],
        "country_code": ["eg", "ma", "dz", "tn", "ly"],
        "company_size": ["1-10", "11-50", "51-200", "201-500"],
    }
)["session_id"]

mcp_server_research.session_enrich(
    session_id,
    enrichment_types=["competitive_landscape", "technographics", "strategic_insights"],
)

result = mcp_server_research.session_view_data(session_id)
print(result)
