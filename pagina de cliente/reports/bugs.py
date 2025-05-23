import streamlit as st
from send_email import send

to = "villalonemiliano199@gmail.com"
sender = "Tool"
subject = "Informacion API VIFI"

# Page configuration with a more professional layout
st.set_page_config(
    page_title="Business Advantages",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
    <style>
    /* Global font and color settings */
    * {
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Main container styling */
    .main {
        padding: 2rem 3rem;
        background-color: #fafafa;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2.5rem 0;
        margin-bottom: 3rem;
        background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .main-title {
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .highlight {
        color: #2563EB;
        position: relative;
    }
    
    .highlight::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 6px;
        bottom: -6px;
        left: 0;
        background-color: rgba(37, 99, 235, 0.2);
        border-radius: 3px;
    }
    
    .subtitle {
        font-size: 1.25rem;
        color: #64748B;
        font-weight: 400;
        max-width: 800px;
        margin: 1rem auto 0;
        text-align: center;
    }
    
    /* Card styling */
    .card-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .advantage-card {
        background-color: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        border: 1px solid #f0f0f0;
    }
    
    .advantage-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    }
    
    .icon-container {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.1);
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1E293B;
    }
    
    .card-description {
        color: #64748B;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: auto;
    }
    
    .learn-more {
        color: #2563EB;
        font-weight: 600;
        text-decoration: none;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
    }
    
    .arrow-icon {
        margin-left: 0.5rem;
        transition: transform 0.2s ease;
    }
    
    .learn-more:hover .arrow-icon {
        transform: translateX(3px);
    }
    
    /* Separator styling */
    .separator {
        height: 1px;
        background: linear-gradient(90deg, rgba(226, 232, 240, 0) 0%, rgba(226, 232, 240, 1) 50%, rgba(226, 232, 240, 0) 100%);
        margin: 4rem 0;
    }
    
    /* Contact form styling */
    .contact-title {
        font-size: 2.2rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .contact-subtitle {
        font-size: 1.1rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .contact-highlight {
        color: #00C39A;
        font-weight: 600;
    }
    
    .contact-form-container {
        display: flex;
        background-color: #F8FAFC;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .form-input-label {
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: #334155;
    }
    
    .stButton>button {
        background-color: #0072CE !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 0.375rem !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        background-color: #005bb7 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    .contact-info-card {
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .contact-info-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .contact-info-content {
        font-size: 0.95rem;
        color: #64748B;
        text-align: center;
    }
    
    .contact-icon {
        display: block;
        margin: 0 auto 0.75rem auto;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #EBF5FF;
        text-align: center;
        line-height: 40px;
        color: #0072CE;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .header-container {
            padding: 1.5rem 1rem;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Header section
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Ventajas <span class="highlight">Competitivas</span></h1>
        <p class="subtitle">Soluciones profesionales diseñadas para desarrolladores e instituciones financieras que buscan excelencia</p>
    </div>
    """, unsafe_allow_html=True)

# Advantage cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="advantage-card">
        <div class="icon-container">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h3 class="card-title">Rendimiento Excepcional</h3>
        <p class="card-description">Optimizamos cada milisegundo para ofrecerle respuestas en menos de 120ms, gracias a nuestra infraestructura especializada para operaciones de alta frecuencia y baja latencia.</p>
        <div class="card-footer">
            <a href="#" class="learn-more">
                Más información
                <span class="arrow-icon">→</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="advantage-card">
        <div class="icon-container">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L17 6.5V10.5L22 14.5L19 19.5H5L2 14.5L7 10.5V6.5L12 2Z" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="14" r="3" stroke="#2563EB" stroke-width="2"/>
            </svg>
        </div>
        <h3 class="card-title">Soporte Inteligente</h3>
        <p class="card-description">Nuestro asistente especializado está disponible 24/7 para resolver sus consultas técnicas al instante, reduciendo tiempos de espera y aumentando la productividad de su equipo.</p>
        <div class="card-footer">
            <a href="#" class="learn-more">
                Más información
                <span class="arrow-icon">→</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="advantage-card">
        <div class="icon-container">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" stroke="#2563EB" stroke-width="2"/>
                <path d="M12 17V11" stroke="#2563EB" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="8" r="1" fill="#2563EB"/>
            </svg>
        </div>
        <h3 class="card-title">Modelo Económico Escalable</h3>
        <p class="card-description">Nuestra estructura de precios pay-as-you-go se adapta a sus necesidades, desde startups en fase de desarrollo hasta soluciones enterprise con soporte prioritario garantizado.</p>
        <div class="card-footer">
            <a href="#" class="learn-more">
                Más información
                <span class="arrow-icon">→</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Separator
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Contact section header
st.markdown("""
    <h2 class="contact-title">Contacta a <span class="contact-highlight">Nuestro Equipo</span></h2>
    <p class="contact-subtitle">Estamos aquí para ayudarte a integrar nuestra API en tus sistemas</p>
    """, unsafe_allow_html=True)

# Contact form and info cards
form_col, info_col = st.columns([3, 2])

with form_col:
    with st.form("contact_form"):
        st.markdown('<div class="form-input-label">Nombre completo</div>', unsafe_allow_html=True)
        nombre = st.text_input("", label_visibility="collapsed")
        
        st.markdown('<div class="form-input-label">Correo electrónico</div>', unsafe_allow_html=True)
        email = st.text_input("", label_visibility="collapsed", key="email_input")
        
        st.markdown('<div class="form-input-label">Empresa</div>', unsafe_allow_html=True)
        empresa = st.text_input("", label_visibility="collapsed", key="empresa_input")
        
        st.markdown('<div class="form-input-label">¿Cómo podemos ayudarte?</div>', unsafe_allow_html=True)
        mensaje = st.text_area("", label_visibility="collapsed", height=120)
        
        submitted = st.form_submit_button("ENVIAR MENSAJE")
        if submitted:
            # Aquí llamarías a tu función send_email
            st.success("¡Gracias! Tu mensaje ha sido enviado y será atendido a la brevedad.")

with info_col:
    st.markdown("""
    <div class="contact-info-card">
        <div class="contact-icon">📧</div>
        <div class="contact-info-title">Correo</div>
        <div class="contact-info-content">ventas@vifi.com</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-info-card">
        <div class="contact-icon">📞</div>
        <div class="contact-info-title">Teléfono</div>
        <div class="contact-info-content">+1 234 567 890</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-info-card">
        <div class="contact-icon">🕒</div>
        <div class="contact-info-title">Horario</div>
        <div class="contact-info-content">Lun-Vie: 9am - 6pm</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem;">
        <a href="#" style="display: inline-block; background-color: #0072CE; color: white; font-weight: 600; padding: 0.75rem 2rem; border-radius: 0.375rem; text-decoration: none; transition: all 0.2s ease;">
            Agendar
        </a>
    </div>
    """, unsafe_allow_html=True)