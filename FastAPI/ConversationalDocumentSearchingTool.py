OPENAI_API_KEY = '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'

from langchain.llms import OpenAI

llm_model_name = "text-davinci-003"

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import Tool

from langchain.agents import AgentType

llm=OpenAI(model_name=llm_model_name,temperature=0)

from langchain.memory import ConversationBufferMemory
from langchain import OpenAI

memory = ConversationBufferMemory(memory_key="chat_history")

#TOOL USING GPT-RETRIEVAL-PLUGIN TO SEARCH DOCS

import requests

amount_of_chunks = 4

BearerToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.USAsQlOT3rktlmjssKbz-QQrxPzAqtD6O62saVw41sU'

class DocumentSearcher():
    def SearchIndex(query: str):
        url = 'http://localhost:8000/query'
        headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {BearerToken}',
        'Content-Type': 'application/json',}
        data = {'queries': [{'query': f'{query}','filter': {},'top_k': 3}]}
        response = requests.get(url=url, headers=headers, json=data)
        data=response.json()
        query_response = ''
        for result in data['results'][0]['results']:
            query_response += result['text']
        return(query_response)
    #ACCESS GPT-RETRIEVAL SERVER
    #MAKE A REQUEST TO QUERY
    #QUERY IS INPUT BY LLM

#ADDING TOOLS
tools = load_tools([],llm=llm)

DocumentSearchingTool = Tool("DocumentSearchingTool",DocumentSearcher.SearchIndex,"A crucial tool that should always be used if you are asked to use a docuement / article. This tool is useful for finding information about a subject from a document in the databse. The input should be a question asking for the information you need.")

tools.append(DocumentSearchingTool)

agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

#FUNCTION TO ASK LLM
def AskLLM(query: str) -> str:
    response = agent_chain.run(input=query)
    return(response)

# response = agent_chain.run(input=user_input)

# while user_input != 'STOP':
#     user_input = input('Input: ')
#     response =agent_chain.run(input=user_input)

# chain.run(input_documents = docs, question = query)
