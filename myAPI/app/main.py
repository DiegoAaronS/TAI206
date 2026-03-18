#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc

#Inicializacion o Instancia de la API
app = FastAPI(
    title= 'My first API',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)
