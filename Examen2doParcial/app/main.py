from typing import Optional
from fastapi import FastAPI,status,HTTPException, Depends
import asyncio
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import datetime

app = FastAPI(
    title= 'My Medic API',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

pacientes=[
    {"id":1,"nombre":"Aaron", "numeroCitas":1},
    {"id":2,"nombre":"Lari", "numeroCitas":1},
    {"id":3,"nombre":"Sebas", "numeroCitas":1}
]

citas=[
    {"id":1, "pacienteID":1 ,"fecha":"09-03-2026", "confirmacion":True, "motivo":"Piel sensible", "estado":False}
]

#Modelo de validacion Pydantic
class PacienteBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=5, description="Nombre del usuario")
    numeroCitas: int = Field(..., max_length=3, description="Numero de citas por usuario", example="1")
    

class CitasBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de citas", example="1")
    pacienteID: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    fecha: int = Field(..., le=datetime.now().date, description="Fecha de consulta")
    motivo: str = Field(..., max_length=100, description="Motivo de consulta")
    estado: bool = Field(..., default=False, description="Estado de consulta")
    
Citas = []    

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

@app.get("/v1/citas/", tags=['Citas Medicas'])
async def consultaCitas(usuarioAuth:str = Depends(verificar_Peticion)):
    return{
       "status":"200",
       "total":len(citas),
       "data":citas
    }

@app.post("/v1/citas/", tags=['Citas Medicas'])
async def agregar_citas(cita:CitasBase):
    for cts in citas:
        if cts["id"] == cita.id:
            raise HTTPException(
                status_code=400,
                detail= "The id already exist"
            )
    citas.append(cita)
    return{
        "mensaje":"Cita agregada",
        "datos":"200",
        "status":"200"
    }

@app.put("/v1/citas/{id}", tags=['Citas Medicas'])
async def confirmar_citas(cita:CitasBase):
    for cts in citas:
        if cts["id"] == cita.id:
            raise HTTPException(
                status_code=400,
                detail= "The id already exist"
            )
    citas.append(cita)
    return{
        "mensaje":"Cita agregada",
        "datos":"200",
        "status":"200"
    }

@app.delete("/v1/citas/{id}", tags=['Citas Medicas',status.HTTP_200_OK])
async def eliminar_citas(id: int, usuarioAuth:str = Depends(verificar_Peticion)):
    for idx, cts in enumerate(citas):
        if cts["id"] == id:
            citas.pop(idx)
            return {
                "mensaje": f"Cita eliminada por {usuarioAuth}"
            }
    raise HTTPException(
        status_code=404,
        detail="Citas not found"
    )