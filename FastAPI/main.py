from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import ConversationalDocumentSearchingTool as DocSearcher

@app.get("/llm")
def get_llm_respose(query: str):
    response = DocSearcher.AskLLM(query)
    return({"llm_respose": response})