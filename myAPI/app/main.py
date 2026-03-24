#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

#Inicializacion o Instancia de la API
app = FastAPI(
    title= 'My first API',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

app.include_router(usuarios.router)
app.include_router(misc.router)
