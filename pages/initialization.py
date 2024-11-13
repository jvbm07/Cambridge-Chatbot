import streamlit as st

def initialize_state():
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

    # Page navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "survey"

    if "survey_completed" not in st.session_state:
        st.session_state.survey_completed = False

    if "chatbot_completed" not in st.session_state:
        st.session_state.chatbot_completed = False

    if "nps_completed" not in st.session_state:
        st.session_state.nps_completed = False

    if "user_tries" not in st.session_state:
        st.session_state.user_tries = 0

    if "user_goal_history" not in st.session_state:
        st.session_state.user_goal_history = []

    if "user_data" not in st.session_state:
        st.session_state.user_data = None

    if "goals_counter" not in st.session_state:
        st.session_state.goals_counter = 0


def switch_to_appropriate_page():
    if not st.session_state.current_page == "survey" and st.session_state.survey_completed == False:
        st.switch_page("pages/survey.py")
    if not st.session_state.current_page == "chatbot" and st.session_state.survey_completed == True and st.session_state.chatbot_completed == False:
        st.switch_page("pages/chatbot.py")
    if not st.session_state.current_page == "nps" and st.session_state.chatbot_completed == True and st.session_state.nps_completed == False:
        st.switch_page("pages/nps.py")
    if not st.session_state.current_page == "end_page" and st.session_state.nps_completed == True:
        st.switch_page("pages/save_data.py")

