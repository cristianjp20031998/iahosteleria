import streamlit as st
from openai import OpenAI

# 1. Configuración segura de la clave API
# 1. Configuración segura de la clave API (Cargada desde los secretos del servidor)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Configuración estética de la interfaz web
st.set_page_config(page_title="RespuestaIA - Hostelería", page_icon="🍔", layout="centered")
st.title("🚀 Asistente de Reseñas Inteligente")
st.subheader("Optimiza la reputación online de tu negocio en segundos")

# 3. Formulario de entrada para el hostelero
col1, col2 = st.columns(2)
with col1:
    tipo_negocio = st.selectbox("Tipo de negocio:", ["Restaurante Tradicional", "Bar de Tapas", "Pizzería", "Cafetería", "Restaurante de Alta Cocina", "Pub / Bar de Copas"])
with col2:
    tono = st.selectbox("Tono de la respuesta:", ["Profesional y Formal", "Cercano y Amistoso", "Ingenioso y Educado"])

resena = st.text_area("Pega aquí la reseña de Google Maps o TripAdvisor:", height=150)

# 4. Procesamiento de la IA con control de errores
if st.button("Generar Respuesta Perfecta ✨", use_container_width=True):
    if resena:
        with st.spinner("Redactando la respuesta ideal... 🧠"):
            try:
                # Prompt de ingeniería avanzado con instrucciones de tono
                prompt = f"""
                Eres el gerente de un {tipo_negocio}. 
                Escribe una respuesta para la siguiente reseña de un cliente.
                Usa un tono de comunicación que sea {tono}.
                
                Instrucciones críticas:
                1. Si la reseña es negativa, sé muy empático, pide disculpas de corazón y ofrece una vía de contacto privada para solucionar el problema.
                2. Si es positiva, agradécela con entusiasmo.
                3. Haz sutilmente SEO local mencionando de forma natural el tipo de establecimiento ({tipo_negocio}) en el texto.
                4. Mantén la respuesta concisa, elegante y lista para publicar.
                
                Reseña del cliente: "{resena}"
                """
                
                # Petición a OpenAI
                resultado = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7 # Añade un toque de creatividad controlada
                )
                
                respuesta_final = resultado.choices[0].message.content
                
                # Mostrar resultado en un cuadro destacado
                st.success("¡Respuesta lista para copiar!")
                st.info(respuesta_final)
                st.caption("💡 Truco: Copia este texto y pégalo directamente en tu perfil de Google Business.")
                
            except Exception as e:
                st.error("Ocurrió un problema temporal al conectar con el servidor de IA. Por favor, inténtalo de nuevo en unos momentos.")
    else:
        st.warning("Por favor, introduce el texto de una reseña primero.")