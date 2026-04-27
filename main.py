from fastapi import FastAPI, HTTPException
from models import GenerateRequest
from generators import GenerateValue

app = FastAPI()

@app.post("/generate")
def generate(request: GenerateRequest):
    rows = request.rows
    schema = request.schema
    headers = [field.name for field in schema]
    data = []
    for i in range(rows):
        row = {}
        for field in schema:
            try:
                row[field.name] = GenerateValue(field.type)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
        data.append(row)
    return {"headers":headers, "data":data}
        
@app.get("/")
def root():
    return {"message": "Ura"}

