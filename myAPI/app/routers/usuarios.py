from fastapi import APIRouter
from fastapi import status,HTTPException, Depends
from app.models.usuario import UserBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix= "/v1/users",
    tags= ["CRUD Usuario"]
)

@router.get("/")
async def consultaUsuarios():
    return{
       "status":"200",
       "total":len(usuarios),
       "data":usuarios
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuarios(usuario:UserBase):
    for usr in usuarios:
        if usr["id"] ==  usuario.id:
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