from dataclasses import Field
from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional
import os

load_dotenv()
client = OpenAI()

class MyOutputFormat(BaseModel):
    step : str = Field(..., description="This is ID of step. Example: START, PLAN, OUTPUT, TOOL, etc.")
    content : Optional[str]= Field(None, description="this is optional string has content for the ID")
    tool : Optional[str] = Field(None, description="This field say which tool to call")
    input : Optional[str] = Field(None, description="This filed provides input data to the tool")

def get_weather(city:str):
    weather_url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(weather_url)
    if response.status_code == 200:
        return f"The weather in the {city} is {response.text}"
    else:
        return "Some issue in getting the  weather update."

def run_command(command:str):
    result = os.system(command)
    return result

def get_gold_rate(tool_input:None):
    response = requests.get("https://api.metalpriceapi.com/v1/latest?api_key=c9af6f2f2c7b31702d55f6e641ece0ff&base=INR&currencies=XAU")
    if response.status_code == 200:
        data = response.json()
        return f" the gold rate id {round(data['rates']['INRXAU'],2)}"  # Adjust based on actual response structure
    else:
        return "some issue in getting gold rate"

available_tools ={
    "get_weather": get_weather,
    "run_command": run_command,
    "get_gold_rate": get_gold_rate
}

SYSTEM_PROMPT = """
You are an expert AI assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN is done, finally you can provide your OUTPUT.
You can also call list of tools if required from  the  list of tools available.
for every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user give the input), PLAN (That can be multiple times) and OUTPUT (after enough PLAN is done).

Output JSON format:
{"step":"START" | "PLAN" | "OUTPUT" | "TOOL", "content":"string", "tool":"string", "input":"string"}

Available tools:
get_weather (city :str) : Takes city as inout string and get teh  current weather of teh  city.
run_command (command :str) : Takes system linux command as input string and run the command and return the result.
get_gold_rate(): Get the gold rate

Example 1:
START: what is the weather of Delhi?
PLAN: {"step":"PLAN":"content":"Seems to be user interested in knowing the  weather of Delhi."}
PLAN: {"step":"PLAN":"content":"Lets see what tool is available for getting the  weather of Delhi."}
PLAN: {"step":"PLAN":"content":"I need to call get_weather tool by passing delhi as input."}
PLAN: {"step":"TOOL":"tool":"get_weather","input":"delhi"}
PLAN: {"step":"OBSERVE":"tool":"get_weather","output":"The weather of Delhi is cloudy and 20 degree celsius"}
PLAN: {"step":"PLAN":"content":"Great!, got the  weather of Delhi."}
OUTPUT: {"step":"OUTPUT":"content":"The weather of Delhi is cloudy and 20 degree celsius"}
"""
print("\n\n\n")
message_history = [
    {"role":"system", "content":SYSTEM_PROMPT},
]
user_query=input("👉 ")
message_history.append({"role":"user", "content":user_query})
while True:
    response = client.chat.completions.parse(
        model="gpt-4o",
        response_format=MyOutputFormat,
        messages=message_history
    )
    # print(f'response: {response}')
    raw_result=response.choices[0].message.content
    # print(f'Raw result : {raw_result}')
    message_history.append({"role":"assistant", "content":raw_result})
    # print(f'message history : {message_history}')
    parsed_result=response.choices[0].message.parsed
    # print(f'Parsed result:{parsed_result}')
    if parsed_result.step == "START":
        print(f'🐣{parsed_result.content}')
        continue

    if parsed_result.step == "PLAN":
        print(f'🐣{parsed_result.content}')
        continue
    if parsed_result.step== "TOOL":
        tool_to_call=parsed_result.tool
        tool_input=parsed_result.input
        print(f"🐣{tool_to_call} is {tool_input}")
        tool_response=available_tools[tool_to_call](tool_input)
        message_history.append({"role":"assistant", "content":tool_response})
        continue
    if parsed_result.step == "OUTPUT":
        print(f'🐣{parsed_result.content}')
        break
print("\n\n\n")