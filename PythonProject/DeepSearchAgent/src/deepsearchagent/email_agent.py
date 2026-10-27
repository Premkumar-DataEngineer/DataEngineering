from agents import Agent
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
from .messenger import send_email


load_dotenv(override=True)
MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME")
EMAIL_NOTIFY = os.getenv("EMAIL_NOTIFY", False)

