# Create server parameters for stdio connection
import os
import dotenv

dotenv.load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import asynccontextmanager
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessageChunk
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool, StructuredTool

# model = ChatOpenAI(model="gpt-4o", temperature=0)
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

# Get the install path of uv by running `which uv` in the terminal
import subprocess

uv_path = subprocess.check_output(["which", "uv"]).decode().strip()

# Get working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

print(working_dir)

server_params = StdioServerParameters(
    command=uv_path,
    # Make sure to update to the full absolute path to your math_server.py file
    args=[
        "run",
        "--directory",
        working_dir,
        "mcp",
        "run",
        "research_server.py",
    ],
)

graph = None


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(
                model, tools, checkpointer=MemorySaver(), debug=True
            )
            inputs = {
                "messages": [
                    SystemMessage(
                        content="You are a helpful sales development research assistant who answers questions by using the Explorium API."
                    ),
                    HumanMessage(
                        content="Give me embedded software development companies in Texas. Tell me about their tech stack"
                    ),
                ]
            }

            # Get the generator and print its contents
            async for msg, metadata in agent.astream(
                inputs,
                stream_mode="messages",
                config={"configurable": {"thread_id": "1"}},
            ):
                if (
                    isinstance(msg, AIMessageChunk)
                    and msg.content
                    # Stream all messages from the tool node
                    and metadata["langgraph_node"] == "tools"
                ):
                    print(msg.content, end="|", flush=True)


from typing import Literal
from src.explorium_mcp_server.tools_businesses import autocomplete as autocomplete_impl


@tool
def autocomplete(
    field: Literal[
        "country",
        "region_country_code",
        "google_category",
        "naics_category",
        "linkedin_category",
        "job_title",
        "company_size",
        "company_revenue",
        "company_age",
        "job_department",
        "job_level",
    ],
    query: str | int,
):
    """
    Autocomplete values for various business fields based on a query string.
    """
    return autocomplete_impl(field, query)


@tool
def get_search_filters(businesses_description: str):
    """
    Get search filters for the given user query.

    businesses_description (str): A percise natural language description of the companies
    the user is looking for.
    """
    create_filters_agent = create_react_agent(
        model,
        [autocomplete],
        checkpointer=MemorySaver(),
    )
    result = create_filters_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"""
Business Search Filter Generation Instructions
You are tasked with generating business search filters based on user descriptions. Follow these steps precisely:

1. Examine the business description carefully to identify ALL key concepts (industries, locations, specializations).

2. For each concept, use the autocomplete tool to find matching filter values:

    a. For industries/specializations: use linkedin_category (preferred)
    b. For regions/states: use region_country_code
    c. For countries: use country_code


3. You MUST call autocomplete separately for EACH distinct concept.
4. For each concept, select only the most general matching category - avoid overly specific subcategories unless explicitly mentioned.
5. Include ALL relevant concepts in your final filters, even if they seem secondary.
6. Valid filter fields:

    linkedin_category (preferred), google_category, or naics_category (use only ONE)
    region_country_code or country_code
    company_size: ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"]
    company_revenue: ["0-500K", "500k-1M", "1M-5M", "5M-10M", "10M-25M", "25M-75M", "75M-200M", "200M-500M", "500M-1B", "1B-10B", "10B-100B", "100B-1T", "1T-10T", "10T+"]
    company_age: ["0-3", "4-10", "11-20", "20+"]

Use short queries to ensure values the autocomplete tool returns values.
Include ONLY filter fields and values returned by autocomplete or from the valid enum values.
Never make up or assume values - only use exact matches from autocomplete results.

Continually evaluate the results of the autocomplete tool you didn't miss anything from
the input query.


Query: {businesses_description}
REMEMBER: you must do your best to include all concepts from the input query in the filters.
If the user specified multiple industry categories, you must continually evaluate the results of the autocomplete tool
to ensure you didn't miss anything from the input query. If you did, call the autocomplete tool again.

Return valid JSON and no other text.
"""
                )
            ]
        },
        config={"configurable": {"thread_id": "1"}},
    )

    response = result["messages"][-1].content
    # return response
    # # Use an LLM to clean the response so it's only fields and values.
    clean_response = model.invoke(
        [
            HumanMessage(
                content=f"""
                Convert this response into valid JSON.
                Acceptable fields are:
                - country
                - region_country_code
                - google_category
                - naics_category
                - linkedin_category
                - job_title
                - company_size
                - company_revenue
                - company_age
                - job_department
                - job_level
                Do not include any other text.
                
                {response}
                """
            ),
        ]
    )
    return {"filters": clean_response.content}


@asynccontextmanager
async def make_graph():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            # Remove start_research_session from tools
            tools = [tool for tool in tools if tool.name not in ["autocomplete"]]
            tools.append(get_search_filters)
            agent = create_react_agent(
                model,
                tools,
                checkpointer=MemorySaver(),
                prompt="""
You are an interactive B2B research expert powered by Explorium's comprehensive business database. Your purpose is to showcase Explorium's powerful data capabilities through engaging, real-time research sessions.
When assisting users:

You may create search sessions for finding companies, or research sessions for specific companies.
For search sessions, you must call get_search_filters to establish baseline filters from the user's query.
For research sessions, you must call create_company_research_session to create a research session for specific companies.
Share the number of matching results at each step
Continuously communicate findings and wait for user input before proceeding
Identify opportunities for data enrichment based on user queries
Suggest relevant enrichment options that would enhance the research

Present yourself as directly connected to Explorium's API, using phrases like:

"I'm searching Explorium's database..."
"Explorium has identified X matching companies..."
"Would you like me to enrich this data with additional insights on...?"

IMPORTANT: When using search sessions, you MUST use the filters returned by get_search_filters.
Do not make up your own filters or use the filters from previous sessions.

Make the demo experience interactive and impressive by highlighting the depth and breadth of Explorium's data capabilities while maintaining a conversational flow. Never mention specific tool names like "get_search_filters" - instead refer to "Explorium API" or "Explorium's database."
""",
            )
            yield agent


if __name__ == "__main__":
    asyncio.run(main())
