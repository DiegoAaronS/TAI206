#Endpoints

from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["Miscellaneous"])

@router.get("/")
async def helloworld():
    return {"mensaje":" Hello world FastAPI"}

@router.get("/v1/welcome")
async def welcome():
    return {"mensaje":" Welcome to your API REST"}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje":"Tu calificacion en TAI es 10"}

@router.get("/v1/parametroO/{id}")
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"User found":id}

@router.get("/v1/parametroOp/")
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"User found":id,"Data":usuario}
        return {"Mensaje":"User not found"}
    else:
        return {"Aviso":"No se proporcionó ID"}