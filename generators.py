from faker import Faker
import random
from models import FieldType

fake = Faker('ru_RU')

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
    func = GENERATORS.get(field_type)
    if func == None:
        raise ValueError(f"Unknown type: {field_type}")
    return func()

