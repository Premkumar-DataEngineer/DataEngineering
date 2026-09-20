import os
import asyncio
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool, SQLiteSession
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv(override=True)

MODEL_NAME= "gpt-5.4-mini"
pushover_user_key = os.getenv("PUSH_OVER_USER_KEY")
pushover_token = os.getenv("PUSH_OVER_TOKEN")
pushover_url="https://api.pushover.net/1/messages.json"
session = SQLiteSession("12345")

@function_tool
def push_tool(message:str)-> str:
    payload = {"user": pushover_user_key, "token": pushover_token, "message": message}
    result=requests.post(pushover_url, data=payload)
    return f"Pushed notification status: {result.status_code}"

async def main():
    agent=Agent(name="Notifier",instructions="You notify user upon request", model=MODEL_NAME, tools=[push_tool])
    with trace("Notifier"):
        result=await Runner.run(agent,"Notify Pizza is ready")
        print(result.final_output)
        result =await Runner.run(agent,"Hi, my name is Prem", session=session)
        print(result.final_output)
        result = await Runner.run(agent, "what is my name?", session=session)
        print(result.final_output)


        # result =  Runner.run_streamed(agent, "Tell a 5 joke")
        # async for event in result.stream_events():
        #     if event.type=="raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        #         print(event.data.delta, end="", flush=True)


asyncio.run(main())



