from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# In-memory phone book
phone_book: Dict[str, str] = {}

# Pydantic model for a single phone number
class PhoneNumber(BaseModel):
    name: str
    number: str

# Pydantic model for multiple phone numbers
class PhoneNumbersList(BaseModel):
    contacts: List[PhoneNumber]

@app.get("/")
def home():
    return {"message": "Welcome to the Phone Book API"}

@app.get("/phones", response_model=dict)
def get_phone_numbers():
    return phone_book

@app.post("/phones")
def add_phone_numbers(phone_list: PhoneNumbersList):
    added_contacts = []
    for phone in phone_list.contacts:
        if phone.name in phone_book:
            raise HTTPException(status_code=400, detail=f"Name '{phone.name}' already exists")
        phone_book[phone.name] = phone.number
        added_contacts.append({"name": phone.name, "number": phone.number})
    
    return {"message": "Phone numbers added", "data": added_contacts}

@app.delete("/phones/{name}")
def delete_phone_number(name: str):
    if name not in phone_book:
        raise HTTPException(status_code=404, detail="Name not found")
    del phone_book[name]
    return {"message": f"Phone number for {name} deleted"}
