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

from typing import TypedDict


class ConfigSchema(TypedDict):
    explorium_api_key: str


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
You are tasked with generating business search filters based on user descriptions. Follow these steps precisely:

1. Examine the business description carefully to identify ALL key concepts (industries, locations, specializations).

2. For each concept, use the autocomplete tool to find matching filter values:

    a. For industries/specializations: use linkedin_category (preferred)
    b. For regions/states: use region_country_code
    c. For countries: use country_code

3. You MUST call autocomplete separately for EACH distinct concept.

4. Choose filters carefully:
    a. Select only the most general matching category for each concept
    b. Avoid overly specific subcategories unless explicitly mentioned
    c. Do not add related categories that weren't mentioned in the description

5. Include ALL relevant concepts from the input query in your final filters.

6. Valid filter fields:
    - linkedin_category (preferred), google_category, or naics_category (use only ONE)
    - country_code: lowercase ISO 3166-1 alpha-2 codes (e.g., "us", "ca")
    - region_country_code: lowercase ISO 3166-2 country-subdivision codes (e.g., "us-tx", "us-ca")
    - company_size: ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"]
    - company_revenue: ["0-500K", "500k-1M", "1M-5M", "5M-10M", "10M-25M", "25M-75M", "75M-200M", "200M-500M", "500M-1B", "1B-10B", "10B-100B"]
    - company_age: ["0-3", "4-10", "11-20", "20+"]

Use short, focused queries with the autocomplete tool to get the most relevant results.
Response format:
Copyfield: [values]

Double-check your final filters to ensure you haven't missed any concepts from the input query.
Include ONLY filter fields and values returned by autocomplete or from the valid enum values. No explanations or additional text.

Call as many tools as possible at once, instead of calling one tool at a time.
Reply with as little text as possible, as the user will not see your responses.

Query: {businesses_description}
REMEMBER: You must include ALL concepts from the input query in your filters. If multiple industry categories are mentioned, ensure all are represented.
"""
                )
            ]
        },
        stream_mode="updates",
        config={"configurable": {"thread_id": "filters-1"}},
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


from langchain_core.runnables import RunnableConfig


@asynccontextmanager
async def make_graph(config: RunnableConfig):
    # Create new server parameters with the API key
    config_api_key = config.get("configurable", {}).get("explorium_api_key")
    user_server_params = StdioServerParameters(
        command=uv_path,
        args=["run", "--directory", working_dir, "mcp", "run", "research_server.py"],
        env={
            "EXPLORIUM_API_KEY": config_api_key or "Invalid API Key",
        },
    )

    async with stdio_client(user_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            # Remove start_research_session from tools
            # REMOVED TEMPORARILY
            # tools = [tool for tool in tools if tool.name not in ["autocomplete"]]
            # tools.append(get_search_filters)
            agent = create_react_agent(
                model,
                tools,
                checkpointer=MemorySaver(),
                config_schema=ConfigSchema,
                prompt="""
You are an interactive Explorium API agent powered by the Explorium API. Your purpose is to showcase Explorium's powerful data capabilities through engaging, real-time research sessions.

When assisting users:
- Create search sessions for finding companies, or research sessions for specific companies
- For search sessions, call get_search_filters to establish baseline filters
- For research sessions, call create_company_research_session
- Share the number of matching results at each step
- Continuously communicate findings and wait for user input
- Identify opportunities for data enrichment
- Suggest relevant enrichment options
- Answer concisely

Present yourself as directly connected to Explorium's API.
Do not mention tools by name or explicit function names. Don't mention sessions. Use phrases like:
"I'm searching Explorium's database..."
"Explorium has identified X matching companies..."
"Would you like me to enrich this data with additional insights on...?"

IMPORTANT: When using search sessions, you MUST use the filters returned by get_search_filters.
Do not make up your own filters or use filters from previous sessions.

IMPORTANT: Reply in Markdown. You must format your responses in Markdown.
Use markdown tables to display multiple results.
Example:

| Company Name | Location | Revenue |
|--------------|----------|---------|
| Company A    | New York | $100M    |
| Company B    | Los Angeles | $50M    |

When comparing companies, opt to use tables.

""",
            )
            yield agent


if __name__ == "__main__":
    asyncio.run(main())
