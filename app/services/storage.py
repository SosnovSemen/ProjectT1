import threading 
import time
from typing import Dict, Any, List

# Модуль временного хранилища в памяти.
# Хранит сгенерированные данные под уникальным file_id.
# Автоматически удаляет данные через заданное время.

# Глобальный словарь: ключ = file_id, значение = список строк (таблица)
temp_storage: Dict[str,List[Dict[str,Any]]] = {}

def StorageData (file_id: str, data: List[Dict[str,Any]], ttl_seconds: int):
# Сохраняет данные в хранилище и планирует их автоматическое удаление.
	temp_storage[file_id] = data
	timer = threading.Timer(ttl_seconds, lambda: temp_storage.pop(file_id,None))
	timer.daemon = True
	timer.start()

def GetDataStorage (file_id: str) -> List[Dict[str,Any]] | None:
# Возвращает данные по file_id.
	return temp_storage.get(file_id)

def DeleteDataStorage (file_id: str):
	"""
	Немедленно удаляет данные из хранилища.
	"""
	temp_storage.pop(file_id, None)
