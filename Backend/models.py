from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, index=True)

    dudas = relationship("Duda", back_populates="usuario")

class Duda(Base):
    __tablename__ = "dudas"

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="dudas")
