from dotenv import load_dotenv
from agents import Agent
import os

from pydantic import BaseModel, Field

load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME","gpt-5.4-mini")

#Instructions
INSTRUCTIONS = """
You are a senior researcher tasked with  writing a cohesive report for a search query.
You will be provided with the original query and some research.
Generate a comprehensive report based on the  research and the  query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim
for 5 - 10 pages of content, at least 1000 words.
"""

#pydantic clas
class ReportData(BaseModel):
    short_summary: str = Field(description="Short summary of the search query")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="The followed up questions")

#call the  agent
writer_agent = Agent(name="writer_agent", instructions=INSTRUCTIONS, model=MODEL_NAME, output_type=ReportData)

