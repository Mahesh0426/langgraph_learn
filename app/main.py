# from .graph import graph
from app.graph import graph
from app.graph import create_chat_graph
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver


MONGODB_URI = "localhost:27017"
load_dotenv()

def init():
    # check pointer
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer = checkpointer)

    while True:
        user_input = input("> ")
        for event in  graph.stream({"messages": [{"role":"user", "content": user_input}] }, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()
                                
init()