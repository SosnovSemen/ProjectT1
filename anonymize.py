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

