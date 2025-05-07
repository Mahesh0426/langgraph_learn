# from .graph import graph
from app.graph import graph
from app.graph import create_chat_graph
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
import json
from langgraph.types  import Command


MONGODB_URI = "mongodb://admin:admin@localhost:27017"
config ={"configurable":{"thread_id":"6"}}
load_dotenv()

#Chat Loop (init Function)
def init():
    # check pointer
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer = checkpointer)

        state = graph_with_mongo.get_state(config=config)
        # for messages in state.values['messages']:
        #     messages.pretty_print()
        
        last_message = state.values['messages'][-1]
        tool_calls = last_message.additional_kwargs.get("tool_calls",[])

        user_query = None

        for call in tool_calls:
            if call.get("function",{}).get("name") == "human_assistance_tool":
               args = call["function"].get("arguments",{})
               try:
                   args_dict = json.loads(args)
                   user_query = args_dict.get("query")
               except json.JSONDecodeError:
                     print("failed to decode function arguments")
                     
        print("user is Trying to ask", user_query)
        ans = input("Resolution > ")

        resume_command = Command(resume={"data": ans})
        for event in graph_with_mongo.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                    event["messages"][-1].pretty_print()
        
            
                                
init()