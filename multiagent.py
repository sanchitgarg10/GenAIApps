# multiagent.py
from flask import Blueprint, render_template, request
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

multiagent_bp = Blueprint('multiagent', __name__)

class ChatBot():
    model: ChatOpenAI
    messages: list[HumanMessage]
    def __init__(self, model, context):
        self.model = model
        self.messages = [SystemMessage(content=context)]

    def append_user_message(self, message):
        self.messages.append(HumanMessage(content=message))

    def run_and_append(self, iteration):
        if iteration > 1:
            self.messages[-1].content += "\n\nNow, let's focus on developing a detailed plan for the most promising idea discussed."
        response = self.model(messages=self.messages)
        self.messages.append(AIMessage(content=response.content))
        return response

@multiagent_bp.route('/multiagent', methods=['GET', 'POST'])
def multiagent():
    conversation = []
    agent1_role = ""
    agent2_role = ""
    if request.method == 'POST':
        openai_api_key = request.form['api_key']
        agent1_role = request.form['agent1_role'] + "\nKeep responses less than 100 words."
        agent2_role = request.form['agent2_role'] + "\nKeep responses less than 100 words."

        
        llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.6, openai_api_key=openai_api_key)
        agent1 = ChatBot(llm, agent1_role)
        agent2 = ChatBot(llm, agent2_role)

        conversation = []
        iterations = 3
        for i in range(iterations):
            print (i)
            response_agent1 = agent1.run_and_append(i)
            agent2.append_user_message(response_agent1.content)
            conversation.append(f"Agent 1: {response_agent1.content}")
            print(f"Agent 1: {response_agent1.content}")  

            response_agent2 = agent2.run_and_append(i)
            agent1.append_user_message(response_agent2.content)
            conversation.append(f"Agent 2: {response_agent2.content}")
            print(f"Agent 2: {response_agent2.content}") 

        return render_template('multiagent.html',
                           agent1_role=agent1_role,
                           agent2_role=agent2_role,
                           conversation=conversation)

    return render_template('multiagent.html')

