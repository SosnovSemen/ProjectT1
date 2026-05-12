from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Pydantic-модели для валидации запросов и ответов в эдпоинтах генерации.

class FieldType(str, Enum):
# Типы, доступные для генерации.
    FullName = "FullName"
    Number = "Number"
    BirthDate = "BirthDate"
    Address = "Address"
    Phone = "Phone"
    Email = "Email"
    Job = "Job"
    Company = "Company"
class FieldSchema(BaseModel):
# Модель одной колонки таблицы.
    name: str
    type: FieldType
class GenerateRequest(BaseModel):
# Модель запроса на генерацию данных.
    rows: int = Field(..., ge=1, le=500_000)
    fields: List[FieldSchema] = Field(..., min_items=1)
