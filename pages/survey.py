import streamlit as st
from pages.initialization import initialize_state, switch_to_appropriate_page

st.session_state.current_page = "survey"
initialize_state()
switch_to_appropriate_page()
# Collect user input
name = st.text_input("Enter your name:")
organisation = st.text_input("Enter your organisation:")
# age = st.number_input("Enter your age:", min_value=0)
# industry = st.text_input("Enter your industry:")
# role = st.text_input("Enter your role:")

# Generate the conversation
if st.button("Submit"):
    if name and organisation:
        # Store the user info in session state
        st.session_state.user_data = {"name": name, "organisation": organisation}
        
        # Switch to the chatbot page
        st.session_state.survey_completed = True
        st.session_state.current_page = "chatbot"
        st.switch_page("pages/chatbot.py")
        st.rerun()  # This forces a rerun to load the new page

    else:
        st.warning("Please fill in all fields before submitting.")
