from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi import FastAPI, Depends, HTTPException
import torch
from schemas import PreguntaRequest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from database import Base, engine
from models import Usuario, Duda
from schemas import PreguntaRequest, id_duda, id_usuario
from database import async_session
import requests
from dotenv import dotenv_values
import google.generativeai as genai
import traceback
from dotenv import dotenv_values

app = FastAPI()

config = dotenv_values(".env")
GEM_TOKEN = config["cont"]
genai.configure(api_key=GEM_TOKEN)

model = genai.GenerativeModel("gemini-2.0-flash")

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.on_event("startup") #deprecado pero me es más fácil
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/respuestas")
async def generar_texto(request: PreguntaRequest, db: AsyncSession = Depends(get_db)):
    contexto_profe_lengua = (
        "Eres un profesor de lengua amable y claro. Tu nombre es Blas (como el Epi y Blas) y te encantan los juegos de palabras "
        "Usa refranes y dichos populares para enseñar lengua a niños y adolescentes que cursen la materia.\n"
        f"Pregunta: {request.pregunta}\nRespuesta:"
    )
    
    try:
        response = model.generate_content(contexto_profe_lengua)
        respuesta = response.text
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en Gemini: {str(e)}")

    username = request.username.strip()
    result = await db.execute(select(Usuario).where(Usuario.nombre_usuario == username))
    usuario = result.scalars().first()

    if not usuario:
        usuario = Usuario(nombre_usuario=username)
        db.add(usuario)
        await db.flush()  
        await db.refresh(usuario)

    nueva_duda = Duda(pregunta=request.pregunta,respuesta=respuesta,timestamp=datetime.utcnow(),user_id=usuario.id)
    db.add(nueva_duda)
    await db.commit()
    await db.refresh(nueva_duda)

    return {"respuesta": respuesta,"usuario_id": usuario.id,"duda_id": nueva_duda.id}


@app.get("/dudas/", response_model=list[id_duda])
async def listar_dudas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Duda))
    dudas = result.scalars().all()
    return dudas

@app.get("/dudas/usuario/{user_id}", response_model=list[id_duda])
async def dudas_por_usuario(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Duda).where(Duda.user_id == user_id))
    dudas = result.scalars().all()
    return dudas

@app.delete("/duda/{duda_id}")
async def borrar_duda(duda_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Duda).where(Duda.id == duda_id))
    duda = result.scalars().first()
    if not duda:
        raise HTTPException(status_code=404, detail="Duda no encontrada")
    db.delete(duda)
    await db.commit()
    return {"mensaje": f"Duda {duda_id} eliminada correctamente"}