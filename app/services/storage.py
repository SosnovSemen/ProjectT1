import threading 
import time
from typing import Dict, Any, List

temp_storage: Dict[str,List[Dict[str,Any]]] = {}

def StorageData (file_id: str, data: List[Dict[str,Any]], ttl_seconds: int = 10):
	temp_storage[file_id] = data
	timer = threading.Timer(ttl_seconds, lambda: temp_storage.pop(file_id,None))
	timer.daemon = True
	timer.start()

def GetDataStorage (file_id: str) -> List[Dict[str,Any]] | None:
	return temp_storage.get(file_id)

def DeleteDataStorage (file_id: str):
	temp_storage.pop(file_id, None)
