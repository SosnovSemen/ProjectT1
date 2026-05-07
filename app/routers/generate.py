from typing import List
from fastapi import APIRouter, HTTPException
from app.services.generator import GenerateData
from app.models.generate_models import GenerateRequest

router = APIRouter(prefix = "/generate", tags = ['generation'])

@router.post('/')
def generate(request: GenerateRequest):
    try:
        data = GenerateData(request.rows, request.fields)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail=str(e))
    headers = [field.name for field in request.fields]
    return {"headers":headers, "data":data}
