#Importaciones
from fastapi import FastAPI

#Inicializacion
app = FastAPI()

#Endpoints
@app.get("/")
async def helloworld():
    return {"mensaje":" Hello world FastAPI"}

@app.get("/welcome")
async def welcome():
    return {"mensaje":" Welcome to your API REST"}