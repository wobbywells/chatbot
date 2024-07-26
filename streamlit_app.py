import streamlit as st
from openai import OpenAI
from os import getenv

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses via OpenRouter. "
    "To use this app, you need to provide an OpenRouter API key, which you can get [here](https://openrouter.ai). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenRouter API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openrouter_api_key = st.text_input("OpenRouter API Key", type="password")
if not openrouter_api_key:
    st.info("Please add your OpenRouter API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client using OpenRouter.
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenRouter API.
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://your-site-url.com",  # Optional, replace with your site URL
                "X-Title": "Your App Name",  # Optional, replace with your app name
            },
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        # Extract the response content and store it in session state.
        response_content = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(response_content)
        st.session_state.messages.append({"role": "assistant", "content": response_content})
