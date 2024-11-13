import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json
import openai
import yaml
from pages.initialization import initialize_state, switch_to_appropriate_page

st.session_state.current_page = "chatbot"

initialize_state()
switch_to_appropriate_page()
## setup env and config
load_dotenv()
llm = ChatOpenAI()
st.set_page_config(page_title="ALP chatbot", page_icon="🤖")
st.title("ALP chatbot")

config_file_path = 'config/config.yaml'
with open(config_file_path, 'r') as file:
    config = yaml.safe_load(file)

max_tries = config.get('max_tries')
template_string = config.get('prompt_template')

## session_state initial configurations
st.session_state.check_prompt_string = template_string

if "user_tries" not in st.session_state:
    st.session_state.user_tries = 0

if "user_goal_history" not in st.session_state:
    st.session_state.user_goal_history = []

if "user_data" not in st.session_state:
    st.session_state.user_data = None

info_json = st.session_state.user_data
if "chat_history" not in st.session_state and not st.session_state.user_data == None:
    st.session_state.chat_history = [
        AIMessage(content=f"Hello, {info_json['name']}! Welcome to the Cambridge GenAI assistant! We are going to ask you about your three main goals to the program. For each goal, please provide sufficient details, including clear objectives, specific outcomes you aim to achieve, and any relevant context. What is your first goal?"),
    ]

if "goals_counter" not in st.session_state:
    st.session_state.goals_counter = 0

def check_goals_chain(user_input, chat_history):
    check_prompt = ChatPromptTemplate.from_template(st.session_state.check_prompt_string)

    check_chain = check_prompt | llm | StrOutputParser()
    
    try:
        return check_chain.invoke({
            "chat_history": chat_history,
            "user_input" : user_input,
        })

    except openai.APIConnectionError:
        st.warning("Connection error. Server is unstable. Retrying the request.")
        return check_goals_chain(user_input, chat_history)

def summarize_goal():
    prompt = f"summarize the conversation history as the user's goal to the program. Summarize only the users intentions, the AI messages are not important. Chat history: {st.session_state.user_goal_history}"
    try:
        goal = llm.invoke(prompt).content
        return goal

    except openai.APIConnectionError:
        st.warning("Connection error. Server is unstable. Retrying the request.")
        return summarize_goal()
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)

    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)



user_query = st.chat_input("Type your message here...")

if user_query is not None and user_query != "":
    with st.chat_message("Human"):
        st.markdown(user_query)

    if st.session_state.user_tries < int(max_tries):
        
        goals_check = check_goals_chain(user_query, st.session_state.user_goal_history)
        json_data = json.loads(goals_check)
        if json_data['is_goal_aligned']:
            st.session_state.user_tries += 1
    
    else: 
        json_string = '{"is_goal_aligned": true, "is_goal_enough_detailed": true}'
        json_data = json.loads(json_string)
        st.session_state.user_tries = 0

    if json_data['is_goal_aligned'] and not json_data['is_goal_enough_detailed']:
        ai_message = json_data['question_to_ask']
        st.session_state.user_goal_history.append(HumanMessage(content=user_query))
        st.session_state.user_goal_history.append(AIMessage(content=ai_message))

    elif json_data['is_goal_aligned'] and json_data['is_goal_enough_detailed']:
        st.session_state.user_goal_history.append(HumanMessage(content=user_query))
        goal = summarize_goal()
        st.session_state.user_goal_history = []
        # ai_message = f"Please, confirm if the goal is correct: {goal}"
        # with st.chat_message("AI"):
        #     st.markdown(ai_message)
        #     is_confirmed = st.button("confirm")
        #     # is_denied = st.button("restart goal")
            
        #     if is_confirmed:
        st.session_state.goals_counter += 1

        goal_number = "goal-"+str(st.session_state.goals_counter)
        st.session_state.user_data[goal_number] = goal
    
        if st.session_state.goals_counter < 3:
            ai_message = f"Thanks for providing goal number {st.session_state.goals_counter}! What's your next goal?"

        else:
            ai_message = "Thank you for participating in the survey!!"
            st.session_state.chatbot_completed = True
            ## save json
            ## check if the goals are different
        # elif is_denied:
        #     ai_message = f"Let's start again then!\n What's your goal {st.session_state.goals_counter}"
    else:
        ai_message = json_data['question_to_ask']

    with st.chat_message("AI"):
        st.markdown(f"{ai_message}")


    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=ai_message))

if st.session_state.chatbot_completed == True:
    with st.chat_message("AI"):
        for i in range(1,4):
            goal_number = "goal-"+str(i)
            goal = st.session_state.user_data[goal_number]
            st.markdown(f"Goal {i}: {goal}")

    # if st.button("Retry chatbot"):
    #     st.session_state.chatbot_completed = False
    #     st.session_state.user_tries = 0
    #     st.session_state.goals_counter = 0
    #     st.session_state.chat_history = None
    #     st.session_state.goal_history = None
    #     st.session_state.current_page = "chatbot"
    #     st.switch_page("pages/chatbot.py")
    if st.button("Submit"):
        st.session_state.current_page = "nps"
        st.switch_page("pages/nps.py")
        st.rerun()  # This forces a rerun to load the new page





