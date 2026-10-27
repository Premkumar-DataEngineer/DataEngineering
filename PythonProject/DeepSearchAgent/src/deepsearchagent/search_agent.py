from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio
import os
import logging
from typing import Dict
from IPython.display import display_markdown
load_dotenv(override=True)

USE_EMAIL=True
HOW_MANY_SEARCHES=5
MODEL_NAME=os.getenv("DEFAULT_MODEL_NAME")
# MODEL_NAME="gpt-5.4-mini"
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.info("Model name: {}".format(MODEL_NAME))

INSTRUCTIONS="""
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of teh  results. The summary must be 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only the summary. 
"""
task = "Most popular AI agent framework in 2026"
settings = ModelSettings(tool_choice="required")
tools=[WebSearchTool()]

search_agent = Agent(name="Search Agent", instructions=INSTRUCTIONS, tools=tools, model=MODEL_NAME, model_settings=settings)

async def main():
    results = await Runner.run(search_agent, task)
    display_markdown(results.final_output)


if __name__ == "__main__":
    asyncio.run(main())

