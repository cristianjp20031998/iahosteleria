import streamlit as st
from openai import OpenAI

# 1. Configuración segura de la clave API (Desde los secretos del servidor)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================================================================
# 🔑 LLAVERO DE CLIENTES: Aquí controlas quién entra y cuándo caduca.
# Formato -> "contraseña_secreta": "Nombre del Negocio (Fecha de caducidad)"
# =========================================================================
CLIENTES_ACTIVOS = {
    "barpepe77": "Bar Pepe (Activo hasta: 05 Agosto)",
    "cafemaria99": "Cafetería María (Activo hasta: 20 Agosto)"
}

# Inicializar el estado de la sesión para el sistema de login
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "nombre_cliente" not in st.session_state:
    st.session_state["nombre_cliente"] = ""

# 2. PANTALLA DE BLOQUEO / LOGIN
if not st.session_state["autenticado"]:
    st.set_page_config(page_title="Acceso Requerido", page_icon="🔒", layout="centered")
    st.title("🔒 Acceso Restringido")
    st.write("Introduce tu contraseña de cliente para acceder al asistente de IA.")
    
    password_input = st.text_input("Contraseña Mensual:", type="password")
    
    if st.button("Entrar al Asistente 🚀", use_container_width=True):
        # Validamos si la contraseña existe en nuestro llavero inteligente
        if password_input in CLIENTES_ACTIVOS:
            st.session_state["autenticado"] = True
            st.session_state["nombre_cliente"] = CLIENTES_ACTIVOS[password_input]
            st.success("¡Acceso concedido!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta o suscripción caducada. Contacte con el administrador para renovar su clave.")
            
# 3. INTERFAZ REAL DEL ASISTENTE (Solo visible si se loguea correctamente)
else:
    st.set_page_config(page_title="RespuestaIA - Hostelería", page_icon="🍔", layout="centered")
    
    # Barra lateral con información del cliente conectado y botón de salir
    st.sidebar.title("🔑 Panel de Control")
    st.sidebar.info(f"🏢 {st.session_state['nombre_cliente']}")
    
    if st.sidebar.button("🔒 Cerrar Sesión", use_container_width=True):
        st.session_state["autenticado"] = False
        st.session_state["nombre_cliente"] = ""
        st.rerun()

    # Contenido principal de la aplicación web
    st.title("🚀 Asistente de Reseñas Inteligente")
    st.subheader("Optimiza la reputación online de tu negocio en segundos")

    # Formulario de entrada para el hostelero
    col1, col2 = st.columns(2)
    with col1:
        tipo_negocio = st.selectbox(
            "Tipo de negocio:", 
            ["Restaurante Tradicional", "Bar de Tapas", "Pizzería", "Cafetería", "Restaurante de Alta Cocina", "Pub / Bar de Copas"]
        )
    with col2:
        tono = st.selectbox(
            "Tono de la respuesta:", 
            ["Profesional y Formal", "Cercano y Amistoso", "Ingenioso y Educado"]
        )

    resena = st.text_area("Pega aquí la reseña de Google Maps o TripAdvisor:", height=150)

    # Procesamiento de la IA con control de errores
    if st.button("Generar Respuesta Perfecta ✨", use_container_width=True):
        if resena:
            with st.spinner("Redactando la respuesta ideal con Inteligencia Artificial... 🧠"):
                try:
                    # Prompt de ingeniería avanzado con instrucciones de tono y SEO
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
                    
                    # Petición a la API de OpenAI
                    resultado = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    
                    respuesta_final = resultado.choices[0].message.content
                    
                    # Mostrar el resultado en pantalla
                    st.success("¡Respuesta lista para copiar!")
                    st.info(respuesta_final)
                    st.caption("💡 Truco: Copia este texto y pégalo directamente en tu perfil de Google Business.")
                    
                except Exception as e:
                    st.error("Ocurrió un problema temporal al conectar con el servidor de IA. Por favor, inténtalo de nuevo en unos momentos.")
        else:
            st.warning("Por favor, introduce el texto de una reseña primero.")
