from dotenv import load_dotenv
import json
import os
import requests


load_dotenv(override=True)
pushover_user_key = os.getenv("PUSH_OVER_USER_KEY")
pushover_token = os.getenv("PUSH_OVER_TOKEN")
pushover_url="https://api.pushover.net/1/messages.json"

def push(message):
    print(f"push: {message}")
    payload = {"user":pushover_user_key, "token":pushover_token, "message":message}
    requests.post(pushover_url, data=payload)

def record_user_details(email: str, name: str="Not provided", note: str="Not provided"):
    email = email.strip().lower()
    name = name.strip().lower()
    note = note.strip().lower()
    push(f"Recording interest from user {name} with  the email {email} and notes ({note})")
    return "OK"

def record_unknown_questions(question: str):
    question = question.strip().lower()
    push(f"Recording unknown question :  {question}")
    return "OK"

record_user_details_json={
    "name":"record_user_details",
    "description":"Use this tool to record the user like to be in touch and provided his email",
    "parameters":{
        "type":"object",
        "properties":
        {
            "email":{"type":"string","description":"The email of the user like to be in touch"},
            "name":{"type":"string","description":"The name of the user like to be in touch"},
            "notes":{"type":"string","description":"The notes of the user like to be in touch"},
        },
        "required":["email"],
        "additionalProperties":False
    }
}

record_unknown_questions_json={
    "name":"record_unknown_questions",
    "description":"Always use this tool to record the questions that can not be answered",
    "parameters":{
        "type":"object",
        "properties":
            {
                "question":{"type":"string","description":"Capture the question that couldn't be answered"}
            },
        "required":["question"],
        "additionalProperties":False
    }
}

tools = [{"type":"function","function":record_user_details_json},
         {"type":"function","function":record_unknown_questions_json}]

tool_map={"record_user_details":record_user_details,
          "record_unknown_questions":record_unknown_questions}

def handle_tool_call(tool_calls: list)->list:
    results = []
    for tool_call in tool_calls:
        tool_called=tool_call.function.name
        tool_arguments=json.loads(tool_call.function.arguments)
        print(f"tool_called: {tool_called}, tool_arguments: {tool_arguments}", flush=True)
        tool=tool_map.get(tool_called)
        result=tool(**tool_arguments) if tool_called else f"{tool_called} is unknown tool."
        results.append({"role":"tool", "content":json.dumps(result),"tool_call_id":tool_call.id})
    return results



# if __name__=="__main__":
#     load_dotenv()
#     if pushover_token:
#         if pushover_token.startswith("a"):
#             print("Push over token is found and looks good.")
#         else:
#             print("Push over token is NOT found.")
#     else:
#         print("Push over token is NOT found.")
#
#     if pushover_user_key:
#         if pushover_user_key.startswith("u"):
#             print("Push over token is found and looks good.")
#         else:
#             print("Push over token is NOT found.")
#     else:
#         print("Push over token is NOT found.")
#
#     # push("Hey, Navya and Dev are good peoples !!!")
#
#     # print(handle_tool_call_manually(tools))
#     globals()["record_unknown_questions"]("This is not a correct question.")
