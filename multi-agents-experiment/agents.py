from textwrap import dedent
from crewai import Agent

class ALPGoalsAgents():
    def conversation_agent(self):
        return Agent(
            role='Conversation Bot',
            goal='Prompt the user with questions and feedbacks',
            backstory=dedent("""\
                As a Conversation Bot, you should be kind and respectful.
                You should provide a fluid conversation with a human. Sometimes
                you may ask them things, sometimes provide information. You 
                must provide concise and helpful prompts to the conversation"""),
            verbose=True
        )        
    def goal_alignment_validator_agent(self):
        return Agent(
            role='Alignment Validator',
            goal='Check if the users goal is aligned with the program',
            backstory=dedent("""\
                As an Alignment Validator, your analysis will identify 
                whether the goal provided by the user is aligned with the 
                program. You should check if the goal has something to do
                with what the program has to offer or not."""),
            verbose=True
        )
    def goal_details_validator_agent(self):
        return Agent(
            role='Detail Validator',
            goal='Check if the users goal has enough details',
            backstory=dedent("""\
                As a Detail Validator, your analysis will identify 
                whether the goal provided by the user has enough details.
                You want the goals to be precise, so the program can be
                improved with the feedback received."""),
            verbose=True
        )
    def structured_summarizer_agent(self):
        return Agent(
            role='Structure Summarizer',
            goal='Check if the users goal has enough details',
            backstory=dedent("""\
                As a Data Structure Expert, your goal is to put 
                all the info you received into a specific structured format. You
                never provide unstructured answers."""),
            verbose=True
        )
        
