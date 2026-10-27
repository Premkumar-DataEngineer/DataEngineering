import os

from annotated_types import UpperCase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from IPython.display import display_markdown
load_dotenv(override=True)

MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME")
llm=ChatOpenAI(model=MODEL_NAME)

@tool
def get_share_price(share_name:str)->float:
    """Return the share price for a given share name from the  below fake price dict."""
    fake_prices={"AMAZON":20.8,"NETFLIX":23.7,"SUNNXT":10.8}
    return fake_prices.get(share_name.upper(),0.0)

llm_with_tools=llm.bind_tools([get_share_price])
message=[HumanMessage("what is the share price of AMAZON?")]
result=llm_with_tools.invoke(message)
# print(f"Content:{repr(result)}")
# print(f"Tool call:{result.tool_calls}")
message.append(result)
for tool_call in result.tool_calls:
    selected_tool={"get_share_price":get_share_price}[tool_call["name"]]
    print(f"selected tool: {selected_tool}")
    print(type(tool_call))
    #need to pass th  args for teh  selected tool and invoke the tool
    tool_result=selected_tool.invoke(tool_call["args"])
    print(f"Tool result:{tool_result}")
    message.append(ToolMessage(content=str(tool_result),
                               tool_call_id=tool_call["id"]))
    print(f"Message:{message}")

final_result=llm_with_tools.invoke(message)
print(f"Final result:{final_result.content}")
    # then call the  llm to get the  share price

# print(f"Amazon: {get_share_price("AMAZON")}")

# message=[SystemMessage("You are a terse assistant and provide the answer in less number of words"),
#         HumanMessage("What is best self help book")]
# message="Top ten self help books"




