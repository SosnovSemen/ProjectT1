from pydantic import BaseModel
from typing import List
from enum import Enum

class FieldType(str, Enum):
    FullName = "FullName"
    Number = "Number"
    BirthDate = "BirthDate"
    Address = "Address"
    Phone = "Phone"
    Email = "Email"
    Job = "Job"
    Company = "Company"
class FieldSchema(BaseModel):
    name: str
    type: FieldType
class GenerateRequest(BaseModel):
    rows: int
    schema: List[FieldSchema]
