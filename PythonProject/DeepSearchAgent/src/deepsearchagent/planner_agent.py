from agents import Agent
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from deepsearchagent.search_agent import INSTRUCTIONS

load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME")
HOW_MANY_SEARCHES = int(os.getenv("HOW_MANY_SEARCHES",'5'))

INSTRUCTIONS =f"""
you are a research assistant. Given a user query come up with  set of web searches
to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.
"""

class WebSearchItem(BaseModel):
    reason: str=Field(description="Your reasoning for why this search is important to this query"),
    query: str=Field(description="The search term used for Web search"),

class WebSearchPlan(BaseModel):
    search_items: list[WebSearchItem]=Field(description="The search items returned by this plan"),

planner_agent = Agent(name="Planner_agent", instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=WebSearchPlan)
