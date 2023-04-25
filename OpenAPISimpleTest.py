import os, yaml

from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec

with open("D:\WorkFiles\LangChainRepo\OpenAPISpecifications\klarna_openapi.yaml", encoding="utf8") as f:
    raw_openai_api_spec = yaml.load(f, Loader=yaml.Loader)
openai_api_spec = reduce_openapi_spec(raw_openai_api_spec)
    
with open("D:\WorkFiles\LangChainRepo\OpenAPISpecifications\klarna_openapi.yaml", encoding="utf8") as f:
    raw_klarna_api_spec = yaml.load(f, Loader=yaml.Loader)
klarna_api_spec = reduce_openapi_spec(raw_klarna_api_spec)

with open("D:\WorkFiles\LangChainRepo\OpenAPISpecifications\spotify_openapi.yaml",encoding="utf8") as f:
    raw_spotify_api_spec = yaml.load(f, Loader=yaml.Loader)
spotify_api_spec = reduce_openapi_spec(raw_spotify_api_spec)

os.environ['SPOTIPY_CLIENT_ID'] = 'c7a47eb39ab14679925f8b8589c428ef'
os.environ['SPOTIPY_CLIENT_SECRET'] = '3efa7dde37da4bf2adeab74558045e13'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8000/RedirectSuccess'

import spotipy.util as util
from langchain.requests import RequestsWrapper

def construct_spotify_auth_headers(raw_spec: dict):
    scopes = list(raw_spec['components']['securitySchemes']['oauth_2_0']['flows']['authorizationCode']['scopes'].keys())
    access_token = util.prompt_for_user_token(scope=','.join(scopes))
    return {
        'Authorization': f'Bearer {access_token}'
    }

# Get API credentials.
headers = construct_spotify_auth_headers(raw_spotify_api_spec)
requests_wrapper = RequestsWrapper(headers=headers)

endpoints = [
    (route, operation)
    for route, operations in raw_spotify_api_spec["paths"].items()
    for operation in operations
    if operation in ["get", "post"]
]
len(endpoints)

import tiktoken
enc = tiktoken.encoding_for_model('text-davinci-003')
def count_tokens(s): return len(enc.encode(s))

count_tokens(yaml.dump(raw_spotify_api_spec))

from langchain.llms.openai import OpenAI
from langchain.agents.agent_toolkits.openapi import planner
llm = OpenAI(model_name="text-davinci-003", temperature=0.0)

spotify_agent = planner.create_openapi_agent(spotify_api_spec, requests_wrapper, llm)
user_query = input("Input: ")
spotify_agent.run(user_query)


