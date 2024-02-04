from io import StringIO
from openai import OpenAI

import os
import streamlit as st
import time
import uuid
import webbrowser
import yaml


extensions = [
    "css",
    "html",
    "php",
    "py"
]


def config():
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config


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
    st.title(config()['app_name'])
    st.divider()
    open_ai_base_url = st.text_input(
        "**OpenAI Base URL**", key="openai_base_url", value="http://127.0.0.1:1234/v1")
    openai_api_key = st.text_input(
        "**OpenAI API Key**", key="openai_api_key", type="password", value="1234567890")
    openai_button = st.button("Get OpenAI Key", on_click=openai_button_onClick)
    st.divider()
    st.markdown("**Version**  \n0.0.1")
    st.markdown("Using own hosted LLM")
    st.divider()
    st.markdown(f"**Session-ID**  \n{st.session_state.session_id}")
    st.divider()

    developer_button = st.button(
        "Developer", on_click=developer_button_onClick)
    github_button = st.button("Github", on_click=github_onClick)

    st.divider()


# Set App Title
st.title(config()['app_title'])


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# File uploader
uploaded_file = st.file_uploader(
    "Upload your file", accept_multiple_files=False)


if prompt := st.chat_input("Chat with me!"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not open_ai_base_url:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Initialize OpenAI
    client = OpenAI(api_key=openai_api_key,
                    base_url=open_ai_base_url)

    file_content = None

    if uploaded_file is not None:
        file_name = uploaded_file.name
        extension = uploaded_file.name.split('.')

        if extension[1] in extensions:
            with st.expander("Content of the uploaded file"):
                string_io = StringIO(
                    uploaded_file.getvalue().decode("utf-8"))

                string_data = string_io.read()
                st.write(string_data)
                prompt = "{} {}".format(prompt, string_data)

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
        for response in client.chat.completions.create(
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
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
