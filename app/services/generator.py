from typing import List
from faker import Faker
import random
from app.models.generate_models import FieldType, FieldSchema

# Модуль генерации синтетических данных.
# Использует библиотеку Faker для создания реалистичных строк.

fake = Faker('ru_RU')

# Функции-генераторы для каждого типа.
def GenerateFullName() -> str:
    return fake.name()
def GenerateNumber() -> int:
    return random.randint(1, 100000)
def GenerateBirthDate() -> str:
    return fake.date_of_birth(minimum_age = 18, maximum_age = 80).isoformat()
def GenerateAddress() -> str:
    return fake.address()
def GeneratePhone() -> str:
    return fake.phone_number()
def GenerateEmail() -> str:
    return fake.email()
def GenerateJob() -> str:
    return fake.job()
def GenerateCompany() -> str:
    return fake.company()

# Словарь маршрутизации: тип -> соответствующая функция-генератор.
GENERATORS = {
        FieldType.FullName: GenerateFullName,
        FieldType.Number: GenerateNumber,
        FieldType.BirthDate: GenerateBirthDate,
        FieldType.Address: GenerateAddress,
        FieldType.Phone: GeneratePhone,
        FieldType.Email: GenerateEmail,
        FieldType.Job: GenerateJob,
        FieldType.Company: GenerateCompany,
        }

def GenerateValue(field_type: FieldType):
# По нужному типу вызывает соответствующий генератор.
    func = GENERATORS.get(field_type)
    if func == None:
        raise ValueError(f"Unknown type: {field_type}")
    return func()

def GenerateData(rows: int, schema: List[FieldSchema])->List[dict]:
# Генерирует полную таблицу данных. Каждый словарь с списке - строка таблицы.
    data = []
    for i in range(rows):
        row = {}
        for field in schema:
            row[field.name] = GenerateValue(field.type)
        data.append(row)
    return data
