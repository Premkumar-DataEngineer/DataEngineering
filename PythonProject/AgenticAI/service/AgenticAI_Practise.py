from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from IPython.display import Markdown, display

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
anoth_apikey = os.getenv("ANOTH_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
    )
if not anoth_apikey:
    print(
        "Anthropic Key is not set. Copy .env.example to .env and add your key."
    )

client = OpenAI(api_key=api_key)
question = ("Ask a highly intelligent question to LLM, it should not be Math puzzle "
            "But some thought provoking question"
            "The question should be short and Indian history based")
model_name="gpt-5.5"
response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "user", "content": question},
    ]
)
competitors=[]
answer=[]
def records(model_name, question):
    competitors.append(model_name)
    answer.append(question)
    print(question)
    display(Markdown("Question: " + question).data)

records(model_name, response.choices[0].message.content)


