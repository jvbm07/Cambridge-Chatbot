import streamlit as st
import json
import os
from pages.initialization import initialize_state, switch_to_appropriate_page
from streamlit_gsheets import GSheetsConnection
from typing import List
from langchain_core.messages import AIMessage, HumanMessage


def process_chat_history(chat_history: List) -> str:
    formatted_messages = []
    for message in chat_history:
        if isinstance(message, HumanMessage):
            sender = "Human"
        elif isinstance(message, AIMessage):
            sender = "AI"
        else:
            continue  # Skip unknown message types

        # Extract the content
        content = message.content

        # Append formatted message
        formatted_messages.append(f"{sender}: {content}")

    # Join all messages with a separator
    return " | ".join(formatted_messages)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

st.session_state.current_page = "end_page"

initialize_state()
switch_to_appropriate_page()
user_data = st.session_state.user_data
chat_history = st.session_state.chat_history

# Process the chat history and store in user_data
formatted_chat = process_chat_history(chat_history)
user_data["chat-history"] = formatted_chat

# Output the formatted chat history
print(user_data["chat-history"])

# Store in user_data
st.write("Thanks for providing your goals! This information will be really useful to improve our course!")
# File path where you want to store the user data
file_path = 'data/users_data.json'

# Step 1: Load existing data from the JSON file, if it exists
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)  # Load existing data
        except json.JSONDecodeError:
            data = []  # If file is empty or corrupted, start with an empty list
else:
    data = []  # If the file doesn't exist, create an empty list

# Step 2: Append the new user data to the existing data
data.append(user_data)

# # Step 3: Save the updated data back to the JSON file
# with open(file_path, 'w') as file:
#     json.dump(data, file, indent=4)  # Use indent=4 for pretty printing (optional)

df = conn.read()
user_data = list(user_data.values())
df.loc[len(df)] = user_data
conn.update(data=df)
