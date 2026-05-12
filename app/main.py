from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import generate
from fastapi import FastAPI

# Главный модуль приложения. Подключает роутеры, монтирует статику.

app = FastAPI()

app.include_router(generate.router) 
        
app.mount("/static",StaticFiles(directory = "app/static"), name = "static")

@app.get("/")
def root():
    return FileResponse("app/static/test.html")
