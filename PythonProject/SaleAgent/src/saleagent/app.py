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

send_email("Test Email from Sales Agent", "Sending out an test email from Sales Agent")