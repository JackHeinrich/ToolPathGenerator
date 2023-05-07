from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import ConversationalDocumentSearchingTool as DocSearcher

import tkinter as tk
from tkinter import filedialog

#FILE PROMPT SETUP
root = tk.Tk()
root.withdraw()

app = FastAPI(docs_url='/docs1')

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/llm")
def get_llm_respose(query: str):
    response = DocSearcher.AskLLM(query)
    return({"llm_respose": response})