from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.types  import interrupt
from langgraph.prebuilt import ToolNode, tools_condition

#define a callable tool that can be invoked by the LLM
@tool
def human_assistance_tool(query: str):
    """Request assistance from a human."""
    human_response = interrupt({"query": query})  # Pauses the graph and saves state
    return human_response["data"]  # Resumes with human-provided data

# Define the tools
tools = [human_assistance_tool]



# Initialize the chat model
llm = ChatOpenAI(model="gpt-4", temperature=0.7,)

#  Tool Binding
llm_with_tool = llm.bind_tools(tools=tools)

# Define the state graph Structure
class State(TypedDict):
   messages: Annotated[list, add_messages]  # Metadata

#Define the Chatbot Function
def chatbot (state:State):
#    messages = state.get("messages") # Read the current messages
#    response = llm.invoke(messages)  #sends the messages to the model to gets a response
#    return {"messages":[response]}   # Return a new state
   # return {"messages": [llm.invoke(state["messages"])]}
      message = llm_with_tool.invoke(state["messages"])  #sends the messages to the model to gets a response
      assert len(message.tool_calls) <= 1
      return {"messages":[message]}   

tool_node = ToolNode(tools=tools)

# Initialize the graph with the chatbot state definition
graph_builder = StateGraph(State)

# Add the Add the Chatbot Node to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

#Define the start and end nodes
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

#without any memory
graph = graph_builder.compile()
# graph.interrupt_after_nodes ("confirm_transaction")

#create a new graph with a checkpointer
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
