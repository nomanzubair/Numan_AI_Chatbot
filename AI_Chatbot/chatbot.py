
import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Page configuration
st.set_page_config(page_title="Num@nAI Chatbot", page_icon="🤖")
st.title("🤖 Num@nAI Assistant")
st.caption("Powered by Azure OpenAI & Streamlit")

# Load environment variables
load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

if not all([api_key, endpoint, deployment]):
    st.error("Azure API key, Endpoint, or Deployment Name is missing in environment variables.")
    st.stop()

# Initialize OpenAI client
@st.cache_resource
def get_client():
    return OpenAI(
        api_key=api_key,
        base_url=endpoint
    )

client = get_client()

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Num@nAI, an intelligent and helpful AI assistant. "
        "Always identify yourself as Num@nAI. "
        "Detect the language used by the user in their message, "
        "and automatically respond in that exact language."
    )
}

# Initialize chat session history
if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_PROMPT]

# Display previous messages (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input field
if user_input := st.chat_input("Type your message here..."):
    # Display user message in UI
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to session history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Num@nAI is thinking..."):
            try:
                response = client.chat.completions.create(
                    model=deployment,
                    messages=st.session_state.messages,
                    max_tokens=500
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                
                # Add assistant response to session history
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                # Remove last failed user message to prevent retry errors
                st.session_state.messages.pop()
                st.error(f"API Error: {e}")
