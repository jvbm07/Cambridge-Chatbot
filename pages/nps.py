# nps.py
import streamlit as st
from pages.initialization import initialize_state, switch_to_appropriate_page

st.session_state.current_page = "nps"
initialize_state()
switch_to_appropriate_page()

# Title of the app
st.title("User Experience Survey")

# Create a form in Streamlit

# Add a slider for the score (1-10)
score = st.slider("Rate your experience (1-5)", min_value=1, max_value=5, step=1)

# Add a text area for additional comments
comments = st.text_area("Additional Comments")
    
# Submit button for the form
if st.button("Submit"):

    st.session_state.user_data.update({
        "nps_score": score,
        "nps_comments": comments
    })
    st.session_state.current_page = "end_page"
    st.session_state.nps_completed = True
    st.switch_page("pages/save_data.py")
