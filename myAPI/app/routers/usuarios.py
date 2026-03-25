from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.usuario import UserBase
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB
from app.security.auth import verificar_Peticion
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/v1/users",
    tags=["CRUD Usuario"]
)

@router.get("/")
async def consulta_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioDB).all()
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

@router.get("/{id}")
async def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuarioP: UserBase, db: Session = Depends(get_db)):
    nuevo_usuario = UsuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {
        "mensaje": "User added",
        "datos": nuevo_usuario
    }

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_completo(
    id: int,
    usuario_data: UserBase,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    usuario.nombre = usuario_data.nombre
    usuario.edad = usuario_data.edad
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "User updated",
        "datos": usuario,
        "status": "200"
    }

class UserPatch(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario_parcial(
    id: int,
    usuario_data: UserPatch,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    if usuario_data.nombre is not None:
        usuario.nombre = usuario_data.nombre
    if usuario_data.edad is not None:
        usuario.edad = usuario_data.edad
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "User partially updated",
        "datos": usuario,
        "status": "200"
    }

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int,
    usuarioAuth: str = Depends(verificar_Peticion),
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    db.delete(usuario)
    db.commit()
    return {
        "mensaje": f"User deleted by {usuarioAuth}"
    }