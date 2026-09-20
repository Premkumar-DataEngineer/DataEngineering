import os
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool, SQLiteSession
load_dotenv(override=True)

