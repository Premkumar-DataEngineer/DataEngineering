from agents.extensions.visualization import draw_graph
from dotenv import load_dotenv
import requests
from agents import Agent, Runner, trace, function_tool, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
import os
import asyncio
import smtplib
from email.message import EmailMessage
load_dotenv(override=True)

MODEL_NAME="gpt-5.4-mini"
EMAIL_ADDRESS =os.environ.get("EMAIL_ADDRESS")
EMAIL_SMPT_SERVER = os.environ.get("EMAIL_SMPT_SERVER")
EMAIL_APP_PWD = os.environ.get("EMAIL_APP_PWD")
PUSH_OVER_URL = os.environ.get("PUSHOVER_URL")
PUSH_OVER_USER_KEY = os.environ.get("PUSH_OVER_USER_KEY")
PUSH_OVER_TOKEN=os.environ.get("PUSH_OVER_TOKEN")

def push_notification(message:str)-> str:
    payload = {"user":PUSH_OVER_USER_KEY,"token":PUSH_OVER_TOKEN,"message":message}
    result = requests.post(PUSH_OVER_URL,data=payload)
    return f"Status of Push notification: {result.status_code}"

def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(body)
    with smtplib.SMTP(EMAIL_SMPT_SERVER, 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PWD)
        smtp.send_message(msg)

def send_message( subject:str, body:str, USE_EMAIL:str = False):
    if USE_EMAIL:
        send_email(subject, body)
    else:
        push_notification(f"Subject: {subject} \n\n {body}")

#send_message(USE_EMAIL=False,subject="Test Email from Sales Agent",body="Sending out an test email from Sales Agent")


intro=("""
You are a Sales Agent working for complAI,
a company that provide SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
You write generic emails, there is no recipient, goal is to increase the sales and no other key points.
""")
instruction1 = intro + "your email style is professional, serious, with gravitas and creditability."
instruction2= intro + "your email style is witty, engaging and humorous."
instruction3= intro + "your email style is concise, to the point and in the style of busy senior executive."

saleagent1=Agent("Professional Sales Agent",instructions=instruction1, model=MODEL_NAME)
saleagent2=Agent("Humorous Sales Agent",instructions=instruction2, model=MODEL_NAME)
saleagent3=Agent("Senior Executive Agent",instructions=instruction3, model=MODEL_NAME)

decision = """
You pick the best cold sate email from the  given option.
Imagine you are a customer and pick one email for which you most likely to respond to.
Do not give any explanation, reply with the selected email only.
You can use the tool to send the email or notification.
"""
sales_picker=Agent("Sales Picker",instructions=decision, model=MODEL_NAME)

@function_tool
def send_email_tool(subject:str, body:str)->str:
    """
    Send out an email with provided subject and body to all sales prospects.
    :param subject: The subject of the email.
    :param body: The body of the email, as plain text.
    :return: String
    """
    send_message(subject=subject, body=body)
    return "Email sent successfully."

require_tool = ModelSettings(tool_choice="required")
sales_sender = Agent("Sales Sender", instructions=decision, model=MODEL_NAME, tools=[send_email_tool],
                     model_settings=require_tool)


async def sale_agent_call(input_msg:str)->None:
    result=Runner.run_streamed(saleagent1,input=input_msg)
    async for event in result.stream_events():
        if event.type=="raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

async def sale_agents_call(input_msg:str)->None:
    with trace("sale_agents_call"):
        results = await asyncio.gather(
            Runner.run(saleagent1,input=input_msg),
        Runner.run(saleagent2,input=input_msg),
        Runner.run(saleagent3,input=input_msg)
        )
        outputs = [result.final_output for result in results]
        emails=f"Cold Sales emails:\n\nEmails:\n\n".join(outputs)
        # best_email=await Runner.run(sales_picker,input=emails)
        await Runner.run(sales_sender, input=emails)
description = """
 Use this tool to write a sales email, in the input just instruct to write a sales email.
 """
tool_name_v1=saleagent1.as_tool(tool_name="sales_agent1",tool_description=description)
tool_name_v2=saleagent2.as_tool(tool_name="sales_agent2",tool_description=description)
tool_name_v3=saleagent3.as_tool(tool_name="sales_agent3",tool_description=description)
tools=[tool_name_v1,tool_name_v2,tool_name_v3, send_email_tool]
instructions="You are a Sales Manager working for complAI, your work is to find a single best cold sale email using the  sales email writer tools."

task = """
Follow these steps:

1. Generate Drafts: Use each of the three sale_email_writer tools to generate different email draft.
Just instruct each to write a sale email: no further details are needed.
Do not proceed until all three drafts are ready, one from each tool.

2. Evaluate and Select: Review the drafts and select one of the best email using your own judgement of which one is most effective.

3. Use your tools to send the best email (and only the best email) to the user. Only send 1 email.
"""

sales_manager= Agent("Sales Manager", instructions=instructions, tools=tools, model=MODEL_NAME)
async def sales_manager_call()->None:
    with trace("sales_manager_call"):
        results=await Runner.run(sales_manager, task)
        print(results.final_output)
if __name__ == "__main__":
    #asyncio.run(sale_agent_call(instruction2))
    #asyncio.run( sale_agents_call(input_msg="Write a cold sale email"))
    # draw_graph(sales_manager)
    asyncio.run(sales_manager_call())

