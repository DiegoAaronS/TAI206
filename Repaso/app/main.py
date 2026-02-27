# Importaciones
from typing import Optional
from fastapi import FastAPI, status, HTTPException
import asyncio
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Inicialización o Instancia de la API
app = FastAPI(
    title='Biblioteca Digital',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

# Base de datos Ficticia
usuarios = [
    {"id": 1, "nombre_User": "Aaron", "correo": "aaron@mail.com"},
    {"id": 2, "nombre_User": "Lari", "correo": "lari@mail.com"},
    {"id": 3, "nombre_User": "Sebas", "correo": "sebas@mail.com"}
]

libros = [
    {"id": 1, "nombre_libro": "El Gran Gatsby", "autor": "F. Scott Fitzgerald", "anio_publicacion": 1925, "paginas": 218, "estado": "disponible"},
    {"id": 2, "nombre_libro": "1984", "autor": "George Orwell", "anio_publicacion": 1949, "paginas": 328, "estado": "disponible"},
    {"id": 3, "nombre_libro": "To Kill a Mockingbird", "autor": "Harper Lee", "anio_publicacion": 1960, "paginas": 281, "estado": "disponible"}
]

libros = []  # Lista para almacenar los libros
prestamos = []  # Lista para almacenar los préstamos

# Modelo de validación Pydantic para usuarios
class UserBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre_User: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    correo: EmailStr = Field(..., description="Correo del usuario", example="usuario@mail.com")

# Modelo de validación Pydantic para libros
class Libro(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del libro", example="1")
    nombre_libro: str = Field(..., min_length=2, max_length=100, description="Nombre del libro")
    autor: str = Field(..., min_length=2, max_length=50, description="Autor del libro")
    anio_publicacion: int = Field(..., ge=1450, le=datetime.now().year, description="Año de publicación")
    paginas: int = Field(..., gt=1, description="Número de páginas del libro")
    estado: str = Field(..., pattern="^(disponible|prestado)$", description="Estado del libro: disponible o prestado")

# Modelo de validación Pydantic para el préstamo
class Prestamo(BaseModel):
    usuario_id: int = Field(..., gt=0, description="ID del usuario")
    libro_id: int = Field(..., gt=0, description="ID del libro")

# Endpoints para gestionar libros
@app.post("/v1/libros/", status_code=201, tags=['CRUD Libro'])
async def registrar_libro(libro: Libro):
    for existing_libro in libros:
        if existing_libro["nombre_libro"].lower() == libro.nombre_libro.lower():
            raise HTTPException(status_code=409, detail="El libro ya está registrado.")
    
    libros.append(libro.dict())
    return {"mensaje": "Libro registrado correctamente", "status": "201"}

@app.get("/v1/libros/", tags=['CRUD Libro'])
async def listar_libros():
    return {"status": "200", "total": len(libros), "data": libros}

@app.get("/v1/libros/{nombre_libro}", tags=['CRUD Libro'])
async def buscar_libro(nombre_libro: str):
    for libro in libros:
        if libro["nombre_libro"].lower() == nombre_libro.lower():
            return {"status": "200", "data": libro}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/v1/prestamos/", status_code=201, tags=['CRUD Préstamo'])
async def registrar_prestamo(prestamo: Prestamo):
    for libro in libros:
        if libro["estado"] == "prestado" and libro["id"] == prestamo.libro_id:
            raise HTTPException(status_code=409, detail="El libro ya está prestado.")
    
    prestamos.append(prestamo.dict())
    for libro in libros:
        if libro["id"] == prestamo.libro_id:
            libro["estado"] = "prestado"
    
    return {"mensaje": "Préstamo registrado correctamente", "status": "201"}

@app.put("/v1/prestamos/{libro_id}/devolver", status_code=200, tags=['CRUD Préstamo'])
async def devolver_libro(libro_id: int):
    for prestamo in prestamos:
        if prestamo["libro_id"] == libro_id:
            prestamos.remove(prestamo)
            for libro in libros:
                if libro["id"] == libro_id:
                    libro["estado"] = "disponible"
            return {"mensaje": "Libro devuelto", "status": "200"}
    
    raise HTTPException(status_code=409, detail="El préstamo no existe")

@app.delete("/v1/prestamos/{libro_id}", status_code=200, tags=['CRUD Préstamo'])
async def eliminar_prestamo(libro_id: int):
    for prestamo in prestamos:
        if prestamo["libro_id"] == libro_id:
            prestamos.remove(prestamo)
            for libro in libros:
                if libro["id"] == libro_id:
                    libro["estado"] = "disponible"
            return {"mensaje": "Préstamo eliminado", "status": "200"}
    
    raise HTTPException(status_code=409, detail="El préstamo no existe")
