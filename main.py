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
    headers = [field.name for field in schema]
    data = []
    for i in range(rows):
        row = []
        for field in schema:
            fieldType = field.type
            if fieldType == "full_name":
                value = fake.name()
            elif fieldType == "job":
                value = fake.job()
            elif fieldType == "street":
                value = fake.street_address()
            elif fieldType == "city":
                value = fake.city()
            elif fieldType == "company":
                value = fake.company()
            elif fieldType == "birth_date":
                value = fake.date_of_birth(minimum_age = 18, maximum_age = 80).isoformat()
            elif fieldType == "email":
                value = fake.email()
            elif fieldType == "phone":
                value = fake.phone_number()
            else:
                value = f"unknown_type_name = {fieldType}"
            row.append(value)
        data.append(row)
    return {"headers":headers, "data":data}

@app.get("/")
def root():
    return {"message": "Ura"}

