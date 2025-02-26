import os
import google.generativeai as genai
from .models import Computador



# Configurar API Keys para poder usar el motor de gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def obtener_respuesta_ia(pregunta):
    
    #Consultaronsulta la base de datos de Computadores y genera una respuesta con Gemini.
    
    # Obtener  el listado de todos los computadores
    computadoras = Computador.objects.all().values("marca", "cpu", "ram", "gb", "precio", "stock", "gpu")

    # Convertir los datos en un formato entendible para la IA
    contexto = "Lista de computadoras en stock:\n"
    for c in computadoras:
        contexto += f"- {c['marca']} | CPU: {c['cpu']} | RAM: {c['ram']}GB | Almacenamiento: {c['gb']}GB | GPU: {c['gpu']} | Precio: ${c['precio']} | Stock: {c['stock']}\n"

    # Crear el mensaje para la IA
    mensaje = f"Información sobre computadores:\n{contexto}\n\nPregunta del usuario: {pregunta}"

    try:
        # Enviar la pregunta a Gemini
        modelo = genai.GenerativeModel("gemini-2.0-flash")
        respuesta = modelo.generate_content(mensaje)

        # Verificar si hay respuesta válida
        respuesta_ia = respuesta.text if respuesta and hasattr(respuesta, "text") else "No se pudo obtener una respuesta."

    except Exception as e:
        respuesta_ia = f"Error al obtener respuesta: {str(e)}"

    return respuesta_ia