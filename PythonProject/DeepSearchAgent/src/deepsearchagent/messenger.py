import smtplib

from dotenv import load_dotenv
import os
import requests
from email.message import EmailMessage
load_dotenv(override=True)

EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO_ADDRESS = os.getenv("EMAIL_TO_ADDRESS")
EMAIL_SMPT_SERVER = os.getenv("EMAIL_SMPT_SERVER")


def send_email(subject, text_body, html_body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM_ADDRESS
    msg['To'] = EMAIL_TO_ADDRESS
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')
    with smtplib.SMTP("smtp-mail.outlook.com", 587) as smtp:
        smtp.starttls()
        smtp.login("prem4mchennai@outlook.com", "pdzzaqfazddoaoco")
        smtp.send_message(msg)

PUSH_OVER_URL = os.getenv("PUSH_OVER_URL")
PUSH_OVER_TOKEN = os.getenv("PUSH_OVER_TOKEN")
PUSH_OVER_USER_KEY = os.getenv("PUSH_OVER_USER_KEY")

def send_push_over(message:str):
    payload = {"user": PUSH_OVER_USER_KEY, "token": PUSH_OVER_TOKEN ,"message": message}
    requests.post(PUSH_OVER_URL, json=payload)

if __name__ == "__main__":
    # send_email("Test email", "From Deep search Agent", "Hello world")
    smtp=smtplib.SMTP("smtp-mail.outlook.com", 587)
    status_code, response=smtp.ehlo()
    print(f"Status : {status_code} and response : {response}")
    status_code, response =smtp.starttls()
    print(f"Status : {status_code} and response : {response}")
    status_code, response =smtp.login('prem4mchennai@outlook.com', 'hrrmokdfsgcvguet')
    print(f"Status : {status_code} and response : {response}")



