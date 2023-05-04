from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import tkinter as tk
from tkinter import filedialog

#FILE PROMPT SETUP
root = tk.Tk()
root.withdraw()

#LOADS PDF
def break_down_pdf(filepath: str):
    loader = UnstructuredPDFLoader(file_path)
    #for online pdf: loader = OnlinePDFLoader("LINK TO PDF")
    data = loader.load()
    #FOR BREAKING DOWN PDF
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 375, chunk_overlap = 0)
    texts = text_splitter.split_documents(data)
    return(texts)

#LETS YOU KNOW HOW LONG PDF IS
# print(f'You have {len(data)} document(s) in your data')
# print(f'There are {len(data[0].page_content)} characters in your document')

#AMOUNT OF PIECES PDF IS BROKEN INTO
# print(f'Now you have {len(texts)} document(s) in your data')

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

#API KEYS
OPENAI_API_KEY = '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'

PINECONE_API_KEY = '4961b180-27ff-42fc-9527-67dedb4132a4'

PINECONE_ENV = 'us-west1-gcp-free'

#OPEN AI TO USE WITH LANGCHAIN TO SEARCH VECTORS
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

index_name = "testindex"

#SETS UP INDEX & CLEARS IT


index = pinecone.Index(index_name)

#OPTION TO CLEAR INDEX - MOSTLY FOR TESTING
clear_index = input("Clear index? Y/N: ")

if clear_index == "Y":
    index.delete(delete_all=True)

new_doc = input("New doc? Y/N: ")

if new_doc == "N":
    docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
else:
    file_path = filedialog.askopenfilename()
    texts = break_down_pdf(file_path)
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

from langchain.llms import OpenAI

# from langchain.chains.question_answering import load_qa_chain

#OPTION TO CHOOSE LANGUAGE MODEL
llm_model = input("What LLM Model? DAVINCI/GPT: ")

if llm_model == "GPT":
    llm_model_name = "gpt-3.5-turbo"
else:
    llm_model_name = "text-davinci-003"

# chain = load_qa_chain(llm,chain_type = "stuff", verbose = True)

# query = input("What is your query? ")

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import Tool

from langchain.agents import AgentType

#TOOL USING PINECONE TO SEARCH DOC
class DocumentSearcher():
    def get_similar_docs(query: str):
        docs = docsearch.similarity_search(query, include_metadata = True,k=4)
        final_text = ''
        for doc in docs:
            final_text += doc.page_content
        return(final_text)

llm=OpenAI(model_name=llm_model_name,temperature=0)

tools = load_tools([],llm=llm)

DocumentSearchingTool = Tool("DocumentSearchingTool",DocumentSearcher.get_similar_docs,"Useful for accessing information, evidence, and quotes, from documents, articles, etc. Input must be in the form of a question asking for the information you want.")

tools.append(DocumentSearchingTool)

from langchain.memory import ConversationBufferMemory
from langchain import OpenAI

memory = ConversationBufferMemory(memory_key="chat_history")

agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

agent = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True)

user_input = input('Input: ')

response = agent_chain.run(input=user_input)

while user_input != 'STOP':
    user_input = input('Input: ')
    response = agent_chain.run(input=user_input)

# chain.run(input_documents = docs, question = query)
