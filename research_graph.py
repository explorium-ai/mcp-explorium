# Create server parameters for stdio connection
import dotenv

dotenv.load_dotenv()

import src.explorium_mcp_server.mcp_server_research as research

from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, StructuredTool

model = ChatOpenAI(model="gpt-4o")

from langgraph.graph import StateGraph, MessagesState, START, END


class GraphState(MessagesState):
    # We store the session ID in the state to avoid having to pass it around
    session_id: str


# Tool definitions
tools = [
    StructuredTool.from_function(research.autocomplete),
    StructuredTool.from_function(research.search_businesses),
]


@tool
def should_continue(state: GraphState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: GraphState):
    messages = state["messages"]
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(GraphState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, ["tools", END])
workflow.add_edge("tools", "agent")

app = workflow.compile()
