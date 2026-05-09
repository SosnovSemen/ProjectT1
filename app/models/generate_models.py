from pydantic import BaseModel, Field
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
    rows: int = Field(..., ge=1, le=500_000)
    fields: List[FieldSchema] = Field(..., min_items=1)
