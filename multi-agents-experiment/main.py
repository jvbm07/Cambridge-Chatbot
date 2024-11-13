from dotenv import load_dotenv
from crewai import Crew
from tasks import ALPGoalsTasks
from agents import ALPGoalsAgents
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import json

load_dotenv()
agents = ALPGoalsAgents()
tasks = ALPGoalsTasks()

conversation_agent = agents.conversation_agent()
goal_alignment_validator_agent = agents.goal_alignment_validator_agent()
goal_details_validator_agent = agents.goal_details_validator_agent()

alp_description = '''Making sense of turbulent times

Learn new ways of thinking – how to navigate global financial crises, cyber security threats trade wars and economic sanctions.
Develop innovative strategic responses to adapt to rapid economic and technological change.
Understand an increasingly complex global financial system 
Achieve long-term sustainability for your organisation. 
Building organisational and personal capabilities 

Become an agile and smart leader. 
Know how to establish an ‘ecosystem’ of partners. 
Learn to manage in a networked or matrix environment. 
Explore scientific and technological developments to transform your organisation.
Ensure local success in a global world – understand how to successfully confront local opponents. 
Leading into the
future

Examine your personal leadership style.
Learn to adapt – but remain authentic to who you are.
Explore innovative ways of motivating people in a difficult economic climate.
Examine how reporting systems need to change to remain relevant in today’s globalised environment.  '''

def orchestrator(user_input):

    alignment_agent = agents.goal_alignment_validator_agent()
    alignment_check = tasks.check_goal_alignment_task(alignment_agent, user_input, alp_description)
    print("------------")
    print("------------")

    alignment_crew = Crew(
        agents=[alignment_agent],
        tasks=[alignment_check]
    )
    response = alignment_crew.kickoff()
    response = json.loads(response)
    print(f"--{response}--")
    if not bool(response.is_goal_aligned):
       return ai_response(response["reason"])
        
    details_agent = agents.goal_details_validator_agent()
    details_check = tasks.check_goal_details_task(details_agent, user_input, alp_description)

    details_crew = Crew(
        agents=[details_agent],
        tasks=[details_check]
    )

    response = details_crew.kickoff()
    if not bool(response["is_goal_detailed"]):   
        return ai_response(response["reason"])
    
    st.session_state.goal_counter += 1
    return ai_response(information="Ask the user about his next goal")

def ai_response(information):
    conversation_agent = agents.conversation_agent()
    response = tasks.conversation_task(conversation_agent, information)
    return response

# app config
st.set_page_config(page_title="Streaming bot", page_icon="🤖")
st.title("Streaming bot")

info_json = {
    "name": "Joao",
    "age": 23,
    "role": "Software Engineer",
    "industry": "Edtech",
    "aim-1": "",
    "aim-2": "",
    "aim-3": "",
    "action": ""
}

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content=f"Hello, {info_json['name']}! Welcome to the ALP assistant! We are going to ask you about your three main goals. What is your first one?"),
    ]
if "goal_counter" not in st.session_state:
    st.session_state.goal_counter = 0

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if st.session_state.goal_counter == 3:
    ai_response(information="Thank the user and end conversation")
    ## recap and ask for confirmation
    ## save the json file
    ## end the survey
elif user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(orchestrator(user_query))

    st.session_state.chat_history.append(AIMessage(content=response))

