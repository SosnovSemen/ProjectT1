from fastapi import FastAPI
from pydantic import BaseModel
from faker import Faker
from typing import List

app = FastAPI()
fake = Faker('ru_RU')

class FieldSchema(BaseModel):
    name: str
    type: str
class GenerateRequest(BaseModel):
    rows: int
    schema: List[FieldSchema]

@app.post("/generate")
def generate(request: GenerateRequest):
    rows = request.rows
    schema = request.schema
    headers = [field.name for field in request.schema]
    data = []
    for i in range(rows):
        row = []
        for field in schema:
            fieldType = field.type
            if fieldType == "full_name":
                value = fake.name()
            elif fieldType == "email":
                value = fake.email()
            elif fieldType == "phone":
                value = fake.phone_number()
            else:
                value = f"unknown_{fieldType}"
            row.append(value)
        data.append(row)
    return {"headers":headers, "data":data}

@app.get("/")
def root():
    return {"message": "Ura"}

