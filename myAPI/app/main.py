#Importaciones
from typing import Optional
from fastapi import FastAPI,status,HTTPException
import asyncio
from pydantic import BaseModel,Field

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

#Modelo de validacion Pydantic
class UserBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre:str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad:int = Field(..., ge=0, le=121, description="Edad valida entre 0 y 121")

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

@app.get("/v1/parametroO/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"User found":id}

@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"User found":id,"Data":usuario}
        return {"Mensaje":"User not found"}
    else:
        return {"Aviso":"No se proporcionó ID"}

@app.get("/v1/users/", tags=['CRUD Usuario'])
async def consultaUsuarios():
    return{
       "status":"200",
       "total":len(usuarios),
       "data":usuarios
    }

@app.post("/v1/users/", tags=['CRUD Usuario'])
async def agregar_usuarios(usuario:UserBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail= "The id already exist"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"User added",
        "datos":"200",
        "status":"200"
    }
    
@app.put("/v1/users/{id}", tags=['CRUD Usuario'])
async def actualizar_usuario(id: int, usuario: dict):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx].update(usuario)
            return {
                "mensaje": "User updated",
                "datos": usuarios[idx],
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@app.delete("/v1/users/{id}", tags=['CRUD Usuario'])
async def eliminar_usuario(id: int):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(idx)
            return {
                "mensaje": "User deleted",
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )