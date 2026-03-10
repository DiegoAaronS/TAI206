from typing import Optional
from fastapi import FastAPI,status,HTTPException, Depends
import asyncio
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title= 'My Medic API',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

usuarios=[
    {"id":1,"nombre":"Aaron","motivo":"Piel sensible"},
    {"id":2,"nombre":"Lari","motivo":"Dolores de estomago"},
    {"id":3,"nombre":"Sebas","motivo":"Dolores de espalda"}
]

citas=[
    {"id":1, "usuarioID":1 ,"fecha":"12-02-2026", "confirmacion":"true"}
]

#Modelo de validacion Pydantic
class UserBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=5, description="Nombre del usuario")
    motivo: str = Field(..., max_length=100, description="Motivo de consulta")

class CitasBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de citas", example="1")
    usuarioID: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    
#***************************
#Seguridad con HTTP Basic
#***************************

security = HTTPBasic()

def verificar_Peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "root")
    contraAuth = secrets.compare_digest(credentials.password, "1234")

    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
        )
    return credentials.username    

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

@app.get("/v1/users/", tags=['CRUD Citas',status.HTTP_200_OK])
async def consultaUsuarios(usuarioAuth:str = Depends(verificar_Peticion)):
    return{
       "status":"200",
       "total":len(citas),
       "data":citas
    }

@app.post("/v1/users/", tags=['CRUD Citas'])
async def agregar_usuarios(usuario:CitasBase):
    for usr in citas:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail= "The id already exist"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Cita agregada",
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
                "datos": citas[idx],
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@app.delete("/v1/users/{id}", tags=['CRUD Usuario',status.HTTP_200_OK])
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_Peticion)):
    for idx, usr in enumerate(citas):
        if usr["id"] == id:
            usuarios.pop(idx)
            return {
                "mensaje": f"Citas eliminada por {usuarioAuth}"
            }
    raise HTTPException(
        status_code=404,
        detail="Citas not found"
    )