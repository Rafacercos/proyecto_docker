import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="API y Blas", page_icon="📚", layout="centered")

st.markdown("""
<style>
    .title { text-align: center; font-size: 2.5em; margin-bottom: 10px; }
    .subtitle { text-align: center; font-size: 1.2em; color: #555; margin-bottom: 30px; }
    .respuesta { background-color: #f8f9fa; padding: 15px; border-radius: 10px; }
    .duda-item { background-color: #f1f3f5; padding: 10px; border-radius: 8px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📚 API y Blas</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tu asistente educativo inteligente para resolver dudas de lenguaje</div>', unsafe_allow_html=True)

with st.form("formulario"):
    col1, col2 = st.columns([1, 3])
    with col1:
        username = st.text_input("Usuario", placeholder="Tu nombre de usuario")
    with col2:
        pregunta = st.text_input("Pregunta", placeholder="Escribe tu duda aquí")

    enviar = st.form_submit_button("Consultar")

if enviar:
    if not username or not pregunta:
        st.warning("Por favor, completa los campos.")
    else:
        payload = {"username": username, "pregunta": pregunta}
        try:
            response = requests.post(f"{API_URL}/respuestas", json=payload)
            response.raise_for_status()
            data = response.json()
            st.markdown("#### ✨ Respuesta generada por Blas:")
            st.markdown(f'<div class="respuesta">{data["respuesta"]}</div>', unsafe_allow_html=True)
            st.info(f'🧑 ID de usuario: {data["usuario_id"]} | 🆔 ID de duda: {data["duda_id"]}')
        except Exception as e:
            st.error(f"❌ Error al contactar con la API: {e}")

st.divider()
st.subheader("📖 Consultar dudas registradas")

# Mostrar dudas completas
if st.button("📋 Ver todas las dudas"):
    try:
        res = requests.get(f"{API_URL}/dudas/")
        res.raise_for_status()
        dudas = res.json()
        if dudas:
            for duda in dudas:
                st.markdown(f"""
                <div class="duda-item">
                    <strong>Usuario ID:</strong> {duda['user_id']}<br>
                    <strong>Pregunta:</strong> {duda['pregunta']}<br>
                    <strong>Respuesta:</strong> {duda.get('respuesta', '')}<br>
                    <strong>Fecha:</strong> {duda['timestamp']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay dudas registradas.")
    except Exception as e:
        st.error(f"Error al obtener dudas: {e}")

# Buscar por usuario
st.markdown("#### 🔍 Buscar dudas por ID de usuario")
user_id_filter = st.text_input("ID del usuario")
if st.button("Buscar dudas"):
    if not user_id_filter.isdigit():
        st.warning("El ID debe ser un número.")
    else:
        try:
            res = requests.get(f"{API_URL}/dudas/usuario/{user_id_filter}")
            res.raise_for_status()
            dudas = res.json()
            if dudas:
                for duda in dudas:
                    st.markdown(f"""
                    <div class="duda-item">
                        <strong>Pregunta:</strong> {duda['pregunta']}<br>
                        <strong>Respuesta:</strong> {duda['respuesta']}<br>
                        <strong>Fecha:</strong> {duda['timestamp']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No se encontraron dudas para ese usuario.")
        except Exception as e:
            st.error(f"Error al obtener dudas del usuario: {e}")

# Borrar duda
st.markdown("#### 🗑️ Eliminar una duda por ID")
duda_id = st.text_input("ID de la duda a eliminar")
if st.button("Eliminar duda"):
    if not duda_id.isdigit():
        st.warning("El ID de la duda debe ser un número.")
    else:
        try:
            res = requests.delete(f"{API_URL}/duda/{duda_id}")
            if res.status_code == 200:
                st.success(f"Duda con ID {duda_id} eliminada correctamente.")
            else:
                st.error(f"No se pudo eliminar: {res.json().get('detail', 'Error desconocido')}")
        except Exception as e:
            st.error(f"Error al eliminar la duda: {e}")
