#Importaciones
from typing import Optional
from fastapi import FastAPI
import asyncio

#Inicializacion o Instancia de la API
app = FastAPI(
    title= 'My first API',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

#BD Ficticia
usuarios=[
    {"id":1,"nombre":"Aaron","edad":21},
    {"id":2,"nombre":"Lari","edad":25},
    {"id":3,"nombre":"Sebas","edad":22}
]

#Endpoints
@app.get("/", tags=['Inicio'])
async def helloworld():
    return {"mensaje":" Hello world FastAPI"}

@app.get("/v1/welcome", tags=['Inicio'])
async def welcome():
    return {"mensaje":" Welcome to your API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje":"Tu calificacion en TAI es 10"}

@app.get("/v1/users/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"User found":id}

@app.get("/v1/users_op/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"User found":id,"Data":usuario}
        return {"Mensaje":"User not found"}
    else:
        return {"Aviso":"No se proporcionó ID"}
