from faker import Faker

fake = Faker("ru_RU")

ValidAdress = ["gmail.com" , "mail.ru" , "yandex.ru" , "ya.ru" , "outlook.com" , "icloud.com"]

def mask(value: str)->str:
    if not value:
        return "***"
    if value.count("@") == 1:
        name,adress = value.split("@")
        if name and adress:
            if adress in ValidAdress:
                return name[0] + "****@" + adress
    if value.startswith("+") and value[1:].isdigit():
        if len(value) >= 4:
            return value[:3] + "****" + value[-2:]
    if " " in value and len(value) > 3:
        parts = value.split()
        if len(parts) >= 2 and all(part.isalpha() for part in parts):
            mas = []
            for part in parts:
                if len(part) <= 2:
                    mas.append(part[0] + "***")
                else:
                    mas.append(part[0] + "***" + part[-1])
            return " ".join(mas)
    return value[0]+ "***"

def replacemask(value: str)->str:
    if not value:
        return fake.name()
    if value.count("@") == 1:
        name, adress = value.split("@")
        if name and adress:
            if adress in ValidAdress:
                return fake.email()
    if value.startswith("+") and len(value)>=5:
        if value[1:].isdigit():
            return fake.phone_number()
    if " " in value and len(value)>3:
        parts = value.split()
        if len(parts)>=2 and all(part.isalpha() for part in parts):
            return fake.name()
    return fake.first_name()

