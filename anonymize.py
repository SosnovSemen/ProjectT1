from faker import Faker
def maskirovanie(value: str)->str:
    ValidAdress = ["gmail.com" , "mail.ru" , "yandex.ru" , "ya.ru", "outlook.com", "icloud.com"]
    if not value:
        return "***"
    if value.count("@") == 1:
        name,adress = value.split("@")
        if name and adress:
            if adress in ValidAdress:
                return name[0] + "****@" + adress
    if value.startswitch("+") and value[1:].isdigit():
        if len(value) >= 4:
            return value[:3] + "****" + value[-2:]
    if " " in value and len(value) > 3:
        parts = value.split()
        if len(parts) >= 2 and all(part.isalpha() for part in parts):
            mask = []
            for part in parts:
                if len(part) <= 2:
                    mask.append(part[0] + "***")
                else:
                    mask.append(part[0] + "***" + part[-1])
            return " ".join(mask)
    return value[0]+ "***"

