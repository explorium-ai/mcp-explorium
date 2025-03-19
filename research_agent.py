# Create server parameters for stdio connection
import os
import dotenv

dotenv.load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o")

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


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke(
                {
                    "messages": "Give me embedded software development companies in Texas. Tell me about their tech stack"
                }
            )

            print(agent_response["messages"].pop())


if __name__ == "__main__":
    asyncio.run(main())
