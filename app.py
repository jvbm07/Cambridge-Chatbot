import streamlit as st
from pages.initialization import initialize_state, switch_to_appropriate_page

# Set page config to handle multiple pages
st.set_page_config(page_title="ALP Chatbot", page_icon="🤖", layout="centered")

st.session_state.current_page = "app"

initialize_state()
switch_to_appropriate_page()
# # Session state to keep track of the user's info
# if "user_data" not in st.session_state:
#     st.session_state.user_data = None

# # Page navigation
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "survey"

# if "survey_completed" not in st.session_state:
#     st.session_state.survey_completed = False

# if "chatbot_completed" not in st.session_state:
#     st.session_state.chatbot_completed = False

