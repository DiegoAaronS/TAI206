from fastapi import APIRouter
from fastapi import status,HTTPException, Depends
from app.models.usuario import UserBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

router= APIRouter(
    prefix= "/v1/users",
    tags= ["CRUD Usuario"]
)

@router.get("/")
async def consultaUsuarios(db:Session= Depends(get_db)):
    leer_usuarios= db.query(UsuarioDB).all()
    return{
       "status":"200",
       "total":len(leer_usuarios),
       "data":leer_usuarios
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuarioP:UserBase,db:Session= Depends(get_db)):

    nuevoUsuario=UsuarioDB(nombre= usuarioP.nombre,edad= usuarioP.edad)

    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    return{
        "mensaje":"User added",
        "datos":nuevoUsuario
    }
    
@router.put("/{id}", status_code=status.HTTP_200_OK)
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

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_Peticion)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(idx)
            return {
                "mensaje": f"User deleted for {usuarioAuth}"
            }
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )