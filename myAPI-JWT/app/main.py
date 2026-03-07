from typing import Optional
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Inicialización o Instancia de la API
app = FastAPI(
    title='My first API JWT',
    description='Sámano Hernández Diego Aarón',
    version='1.0'
)

# Configuración para OAuth2 y JWT
SECRET_KEY = "1234" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1/1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para truncar contraseñas largas (bcrypt tiene límite de 72 bytes)
def truncate_password(password: str) -> str:
    if len(password.encode('utf-8')) > 72:
        return password[:72]
    return password

# Base de datos ficticia
usuarios = [
    {"id": 1, "nombre": "Aaron", "edad": 21, "email": "aaron@mail.com", "password": pwd_context.hash("pass123")},
    {"id": 2, "nombre": "Lari", "edad": 25, "email": "lari@mail.com", "password": pwd_context.hash("pass123")},
    {"id": 3, "nombre": "Sebas", "edad": 22, "email": "sebas@mail.com", "password": pwd_context.hash("pass123")}
]

# Modelo Pydantic para el login
class UserBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad: int = Field(..., ge=0, le=121, description="Edad válida entre 0 y 121")

class UserInDB(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    nombre: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = truncate_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    password = truncate_password(password)
    return pwd_context.hash(password)

def get_user_by_email(db, email: str):
    for user in db:
        if user["email"] == email:
            return user
    return None

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(usuarios, form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(id=1, nombre=username)
    except JWTError:
        raise credentials_exception
    return token_data

@app.put("/v1/users/{id}", tags=['CRUD Usuario'])
async def actualizar_usuario(id: int, usuario: dict, current_user: TokenData = Depends(get_current_user)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[idx].update(usuario)
            return {"mensaje": "Usuario actualizado", "status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/users/{id}", tags=['CRUD Usuario'])
async def eliminar_usuario(id: int, current_user: TokenData = Depends(get_current_user)):
    for idx, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(idx)
            return {"mensaje": "Usuario eliminado", "status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")