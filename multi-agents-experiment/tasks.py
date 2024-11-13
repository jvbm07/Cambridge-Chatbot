from textwrap import dedent
from crewai import Task

class ALPGoalsTasks():
  def check_goal_alignment_task(self, agent, user_goal, program_description):
    return Task(
      description=dedent(f"""\
        Check if the goal the user provided is aligned with the program. 
        Inform the user if his goal can be achieved through the program or not.
        Answer using a dictionary with two items, such as is_goal_aligned : boolean and reason: str
        Program Description: {program_description}
        User Goal: {user_goal}
        """),
      expected_output=dedent(f"""\
        The answer should be a dictionary with two items.
        Answer if the goal is aligned or not, as a boolean, and a short reason for it, as a string.
        Return only the dictionary, nothing else. The items are
        is_goal_aligned: bool
        reason: str"""),
      agent=agent,
      async_execution=True
    )
  
  def check_goal_details_task(self, agent, user_goal):
    return Task(
      description=dedent(f"""\
        Check if the goal the user provided has enough details. 
        Inform the user if his goal has enough details or he should rewrite it.
        The goal should have information beyond the final objective, such as the reason why 
        it is important or how the user thinks the program will help him achieve those goals.
        Do not be very rigorous so the user can be discouraged. Only in cases the goal is very
        vague, ask him to rewrite it.               
        User Goal: {user_goal}
        """),
      expected_output=dedent(f"""\
        The answer should be a dictionary with two items.
        Answer if the goal is enough detailed or not, as a boolean, 
        and a short reason for it, as a string.
        Return only the dictionary, nothing else. The items are
        is_goal_detailed: bool
        reason: str"""),
      agent=agent,
      async_execution=True
    )
  
  def conversation_task(self, agent, information):
    return Task(
      description=dedent(f"""\
        Provide a response to the user, giving him relevant information
        Information: {information}
        """),
      expected_output=dedent(f"""\
        The answer should be a response to the user based on the info. 
        The length of the response could be adapted to the information 
        the user wants. Could be short or long, more formal or informal,
        a question, an answer or a request"""),
      agent=agent,
      async_execution=True
    )