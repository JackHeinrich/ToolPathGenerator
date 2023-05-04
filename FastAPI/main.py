from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

import FastAPIPineconeManager as PineconeManager

import tkinter as tk
from tkinter import filedialog

#FILE PROMPT SETUP
root = tk.Tk()
root.withdraw()

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return{"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q:Union[str,None] = None):
    return({"item_id": item_id, "q": q})

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return({"item_price": item.price, "item_id": item_id})

@app.get("/llm")
def get_llm_respose(query: str):
    response = PineconeManager.AskLLM(query)
    return({"llm_respose": response})

@app.post("/pinecone")
def upload_pdf(file_path: str = ''):
    print(file_path)
    PineconeManager.UploadDocument(file_path)
    return({"Status": "Succesfully uploaded document: " + file_path})

@app.put("/pinecone")
def clear_index(index_name: str):
    PineconeManager.ClearIndex(index_name)
    return({"Status": "Succesfuly cleared " + index_name + "."})