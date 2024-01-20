from openai import OpenAI

import config
import os
import streamlit as st
import time
import uuid
import webbrowser


# Variables
API_BASE = config.OPENAI_API_BASE
API_KEY = config.OPENAI_API_KEY


# Initialize OpenAI
openai = OpenAI(api_key=API_KEY, base_url=API_BASE)


# Functions
def openai_button_onClick():
    webbrowser.open("https://platform.openai.com/account/api-keys")


def developer_button_onClick():
    webbrowser.open("https://aprokira.de")


def github_onClick():
    webbrowser.open("https://github.com/xkiiyoshiix")


if "session_id" not in st.session_state:  # Used to identify each session
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:  # Stores the run state of the assistant
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:  # Stores the messages of the assistant
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}]

if "retry_error" not in st.session_state:  # Used for error handling
    st.session_state.retry_error = 0


# Sidebar
with st.sidebar:
    st.caption = "Sidebar"
    st.set_page_config(page_title="Aprokira")
    st.title(config.APP_NAME)
    st.divider()
    st.markdown("**Version**  \n0.0.1")
    st.markdown("Using own hosted LLM")
    st.divider()
    st.markdown(f"**Session-ID**  \n{st.session_state.session_id}")
    st.divider()

    # openai_api_key = st.text_input(
    #    "**OpenAI API Key**", key="chatbot_api_key", type="password", value=API_KEY)
    # openai_button = st.button("Get OpenAI Key", on_click=openai_button_onClick)
    developer_button = st.button(
        "Developer", on_click=developer_button_onClick)
    github_button = st.button("Github", on_click=github_onClick)

    st.divider()


# Set App Title
st.title(config.APP_TITLE)


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Chat with me!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Simulate stream of response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for response in openai.chat.completions.create(
            model="-",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            # Check if message ended
            finish_reason = response.choices[0].finish_reason

            if finish_reason != "stop":
                full_response += response.choices[0].delta.content
                message_placeholder.markdown(full_response)
                # time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
