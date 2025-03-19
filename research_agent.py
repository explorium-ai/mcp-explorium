# Create server parameters for stdio connection
import os
import dotenv

dotenv.load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessageChunk
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
            graph = create_react_agent(
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
            async for msg, metadata in graph.astream(
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


if __name__ == "__main__":
    asyncio.run(main())
