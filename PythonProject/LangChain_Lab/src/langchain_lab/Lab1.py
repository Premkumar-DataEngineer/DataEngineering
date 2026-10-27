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
result=llm_with_tools.invoke("what is the share price of AMAZON?")
print(f"Content:{repr(result)}")
print(f"Tool call:{result.tool_calls}")

# print(f"Amazon: {get_share_price("AMAZON")}")

# message=[SystemMessage("You are a terse assistant and provide the answer in less number of words"),
#         HumanMessage("What is best self help book")]
# message="Top ten self help books"




