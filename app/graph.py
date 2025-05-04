from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# Initialize the chat model
llm = ChatOpenAI(
    model="gpt-4",  
    temperature=0.7,
)

# Define the state graph Structure
class State(TypedDict):
   messages: Annotated[list, add_messages]

#Define the Chatbot Function
def chatbot (state:State):
#    messages = state.get("messages")
#    response = llm.invoke(messages)  #sends the messages to the model to gets a response
#    return {"messages":[response]}
    return {"messages": [llm.invoke(state["messages"])]}

# Initialize the graph with the chatbot state definition
graph_builder = StateGraph(State)

# Add the chatbot function to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

#without any memory
graph = graph_builder.compile()

#create a new graph with a checkpointer
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
