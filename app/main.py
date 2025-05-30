# from .graph import graph
from app.graph import graph
from app.graph import create_chat_graph
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver


MONGODB_URI = "mongodb://admin:admin@localhost:27017"
config ={"configurable":{"thread_id":"6"}}
load_dotenv()

#Chat Loop (init Function)
def init():
    # check pointer
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer = checkpointer)

        while True:
            user_input = input("> ")
            # Streaming the Graph
            for event in  graph_with_mongo.stream({"messages": [{"role":"user", "content": user_input}] }, config, stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()
                                
init()