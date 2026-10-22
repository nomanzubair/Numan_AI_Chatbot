import streamlit
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not all([api_key, endpoint, deployment]):
    raise ValueError(
        "Azure API key, Endpoint, or Deployment Name is missing in the configuration."
    )

client = OpenAI(
    api_key=api_key,
    base_url=endpoint
)

messages = [
    {
        "role": "system",
        "content": (
            "You are Num@nAI, an intelligent and helpful AI assistant."
            "Always identify yourself as Num@nAI."
            "Detect the language used by the user in their message,"
            "and automatically respond in that exact language."
        )
    }
]

print("Num@nAI Active | Azure Chatbot Service Started.")
print("Type 'exit' to terminate the session.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Num@nAI: Thank you! Have a great day ahead, Sir.")
        break

    if not user_input:
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=messages,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        print(f"\nBot: {reply}\n")

        messages.append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:
        messages.pop()
        print(f"\nAPI Error: {e}\n")
