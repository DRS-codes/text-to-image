import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

invoke_url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b"

headers = {
    "Authorization": f"Bearer {NVIDIA_API_KEY}",
    "Accept": "application/json",
}

st.title("🖼️ AI Image Generator Chatbot")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])

# user prompt
prompt = st.chat_input("Describe the image you want...")

if prompt:

    # show user message
    st.chat_message("user").write(prompt)

    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": prompt
    })

    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "steps": 4
    }

    with st.chat_message("assistant"):
        with st.spinner("Generating image..."):

            response = requests.post(
                invoke_url,
                headers=headers,
                json=payload
            )

            response.raise_for_status()
            data = response.json()

            # extract base64 image
            image_base64 = data["artifacts"][0]["base64"]

            # decode image
            image_bytes = base64.b64decode(image_base64)

            st.image(image_bytes)

            st.session_state.messages.append({
                "role": "assistant",
                "type": "image",
                "content": image_bytes
            })

            st.download_button(
                "Download Image",
                image_bytes,
                file_name="generated.png",
                mime="image/png"
            )