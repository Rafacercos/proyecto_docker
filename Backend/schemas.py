from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class PreguntaRequest(BaseModel):
    username: str
    pregunta: str

class usuarioBase(BaseModel):
    nombre_usuario: str

class crear_usuario(usuarioBase):
    pass

class id_usuario(usuarioBase):
    id: int

    class Config:
        orm_mode = True
class dudaBase(BaseModel):
    pregunta: str

class crear_duda(dudaBase):
    user_id: int  

class id_duda(dudaBase):
    id: int
    respuesta: Optional[str] = None
    timestamp: datetime
    user_id: int

    class Config:
        orm_mode = True