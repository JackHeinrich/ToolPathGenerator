from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

import os

os.environ['SERPAPI_API_KEY'] = 'd9fd39c5390a9b48969db2f849d3b5979134d4964484e7a4368535b8547a0ba4'

search = SerpAPIWrapper()
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history")

llm=OpenAI(model_name="text-davinci-003",temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

user_input = input('Input: ')

agent_chain.run(input=user_input)

while user_input != 'STOP':
    user_input = input('Input: ')
    agent_chain.run(input=user_input)