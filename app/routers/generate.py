import csv
import json
import io
import uuid
from typing import List
from app.services.storage import StorageData, DeleteDataStorage, GetDataStorage
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Query
from app.services.generator import GenerateData
from app.models.generate_models import GenerateRequest



router = APIRouter(prefix = "/generate", tags = ['generation'])

# Эндпоинт для генерации данных и получения file_id.
@router.post('/')
def generate(request: GenerateRequest):
# Генерирует все данные, исходя из запроса, сохраняет их во временное хранилище и возвращает file_id и превью таблицы (превые 5 строк).
	try:
		data = GenerateData(request.rows, request.fields)
	except ValueError as e:
		raise HTTPException(status_code = 400, detail=str(e))
	headers = [field.name for field in request.fields]
	file_id = str(uuid.uuid4())
	StorageData(file_id, data, 40)
	preview_table = [[row[head] for head in headers] for row in data]
	return {
		"file_id": file_id,
		"headers": headers,
		"data": preview_table[:5],
	}

# Эндпоинт для скачивания файла в формате CSV и JSON.
@router.get('/download/{file_id}')
def DownloadFile(file_id: str, format: str = Query("csv", pattern = "^(csv|json)$")):
# Скачивает ранее сгенерированные данные в указанном формате.
	data = GetDataStorage(file_id)
	if data is None:
		raise HTTPException(status_code = 404, detail = "File not found or expired")
	if not data:
		raise HTTPException(status_code = 400, detail = "Empty Data")
	headers = list(data[0].keys())
	# Формирование CSV.
	if format == "csv":
		output = io.StringIO()
		writer = csv.writer(output, delimiter=',', quoting = csv.QUOTE_MINIMAL)
		writer.writerow(headers)
		for data_row in data:
			row = [data_row[head] for head in headers]
			writer.writerow(row)
		content = output.getvalue().encode("utf-8-sig")
		media_type = "text/csv"
		filename = f"data_{file_id}.csv"
	# Формирование JSON.
	else: # format == "json"
		result = {"headers": headers, "data": data}
		content = json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8")
		media_type = "application/json"
		filename = f"data_{file_id}.json"
	DeleteDataStorage(file_id)
	return StreamingResponse(io.BytesIO(content), media_type=media_type, headers = {"Content-Disposition": f"attachment; filename={filename}"})
