import streamlit as st
import base64

# Configuración de la página
st.set_page_config(
    page_title="Análisis Bursátil Inteligente",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Raleway:wght@400;500;600&display=swap');
    
    .main {
        padding: 2rem 5rem;
        background-color: white;
    }
    
    .title-black {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 3.5rem;
        line-height: 1.1;
        color: #1E1E1E;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .title-green {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 3.5rem;
        line-height: 1.1;
        color: #4AD295;
        margin-top: 0;
        padding-top: 0;
    }
    
    .subtitle {
        font-family: 'Raleway', sans-serif;
        font-size: 1.2rem;
        font-weight: 500;
        line-height: 1.4;
        color: #1E1E1E;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        max-width: 600px;
    }
    
    .description {
        font-family: 'Raleway', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #333333;
        margin-bottom: 2rem;
        max-width: 600px;
    }
    
    .btn-blue {
        font-family: 'Raleway', sans-serif;
        background-color: #2E77D0;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        margin-right: 1rem;
        text-decoration: none;
    }
    
    .btn-green {
        font-family: 'Raleway', sans-serif;
        background-color: #4AD295;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        margin-right: 1rem;
        text-decoration: none;
    }
    
    .btn-outline {
        font-family: 'Raleway', sans-serif;
        background-color: transparent;
        color: #2E77D0;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        border: 2px solid #2E77D0;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
        text-decoration: none;
    }
    
    .dashboard-image {
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        width: 100%;
    }
    
    .container {
        display: flex;
        gap: 2rem;
    }
    
    .left-column {
        flex: 1;
    }
    
    .right-column {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .investment-text {
        font-family: 'Raleway', sans-serif;
        font-size: 1.2rem;
        font-weight: 500;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .demo-button {
        font-family: 'Raleway', sans-serif;
        background-color: transparent;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: 2px solid white;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        display: block;
        width: fit-content;
        margin: 0 auto;
        text-decoration: none;
    }
    
    .arrow-icon {
        margin-left: 5px;
    }
    
    .phone-icon {
        margin-right: 5px;
    }
    
    .client-icon {
        margin-right: 5px;
    }
    
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .container {
            flex-direction: column;
        }
        
        .title-black, .title-green {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar imagen de dashboard
def get_dashboard_image():
    # Esta es una imagen de ejemplo que representa un dashboard financiero
    # En un caso real, utilizarías una imagen más específica
    dashboard_img_url = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
    return f"<img src='{dashboard_img_url}' class='dashboard-image' alt='Dashboard financiero'>"

# Diseño principal (dos columnas)
col1, col2 = st.columns([1, 1])

# Columna izquierda - Textos y botones
with col1:
    st.markdown("<h1 class='title-black'>ANÁLISIS<br>BURSÁTIL</h1>", unsafe_allow_html=True)
    st.markdown("<h1 class='title-green'>INTELIGENTE</h1>", unsafe_allow_html=True)
    
    st.markdown("<p class='subtitle'>Tecnología de vanguardia para tomar decisiones informadas en los mercados financieros</p>", unsafe_allow_html=True)
    
    st.markdown("<p class='description'>Combina el poder de la inteligencia artificial con análisis técnico avanzado para maximizar tus oportunidades de inversión</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div>
        <a href="#" class="btn-blue">VER VENTAJAS <span class="arrow-icon">→</span></a>
        <a href="#" class="btn-green">DEMO EN VIVO <span class="arrow-icon">↗</span></a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <a href="#" class="btn-outline"><span class="phone-icon">📞</span> PLAN PERSONALIZADO</a>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <a href="#" class="btn-outline"><span class="client-icon">↑</span> ACCESO CLIENTES</a>
    """, unsafe_allow_html=True)

# Columna derecha - Imagen del dashboard
with col2:
    st.markdown("""
    <div style="position: relative; background-color: #333; border-radius: 10px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
        <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80" style="width: 100%; border-radius: 10px;">
        <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); padding: 20px;">
            <p class="investment-text">¿Listo para transformar tu estrategia de inversión?</p>
            <a href="#" class="demo-button">CÓMO FUNCIONA →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)