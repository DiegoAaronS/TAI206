#Modelo de validacion Pydantic
from pydantic import BaseModel, Field
class UserBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre:str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad:int = Field(..., ge=0, le=121, description="Edad valida entre 0 y 121")