import streamlit as st
import json
import os
from pages.initialization import initialize_state, switch_to_appropriate_page
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

st.session_state.current_page = "end_page"

initialize_state()
switch_to_appropriate_page()
st.title("saved data")
user_data = st.session_state.user_data
st.write(user_data)
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


# Step 3: Save the updated data back to the JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)  # Use indent=4 for pretty printing (optional)

df = conn.read()
user_data = list(user_data.values())
df.loc[len(df)] = user_data
conn.update(data=df)
