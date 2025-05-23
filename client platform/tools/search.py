import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Optimización: Configuración de página más eficiente
st.set_page_config(
    page_title="API Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Optimización: CSS simplificado y más eficiente
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main {
        padding: 1rem;
        background-color: #f9fafb;
    }
    
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .welcome-text {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: -0.25rem;
    }
    
    .email-highlight {
        color: #3b82f6;
        font-weight: 500;
    }
    
    .card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: #111827;
    }
    
    .key-container {
        display: flex;
        background-color: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    .warning-text {
        color: #f59e0b;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .warning-icon {
        margin-right: 0.375rem;
    }
    
    .stat-card {
        background-color: white;
        border-radius: 0.375rem;
        padding: 0.875rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        border: 1px solid #f0f0f0;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.125rem;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    .doc-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
    }
    
    .doc-link {
        display: flex;
        align-items: center;
        color: #3b82f6;
        padding: 0.5rem 0;
        text-decoration: none;
        font-size: 0.875rem;
        transition: color 0.15s ease;
    }
    
    .doc-link:hover {
        color: #2563eb;
    }
    
    .doc-link-icon {
        margin-right: 0.5rem;
    }
    
    .progress-container {
        margin: 0.75rem 0;
    }
    
    .progress-labels {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.25rem;
        font-size: 0.75rem;
        color: #6b7280;
    }
    
    .plan-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .plan-name {
        font-weight: 600;
        color: #111827;
    }
    
    .plan-limit {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    /* Optimización botones */
    .stButton>button {
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    /* Ocultar elementos de streamlit innecesarios */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Optimización: Cache para datos que no cambian frecuentemente
@st.cache_data(ttl=300)  # cache durante 5 minutos
def get_api_data():
    """Simulación de obtener datos de API (en un caso real, esto llamaría a un backend)"""
    return {
        "api_key": "sk_live_1234567890abc",
        "api_calls_today": 650,
        "api_calls_month": 12450,
        "usage_percentage": 65,
        "limit_per_day": 1000,
        "plan_name": "Plan Professional",
        "email": "usuario@empresa.com"
    }

# Optimización: Cache para datos de gráfico
@st.cache_data(ttl=600)  # cache durante 10 minutos
def get_chart_data():
    """Obtiene datos para el gráfico de tendencia (simulado)"""
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d-%m') for i in range(7, 0, -1)]
    values = [450, 520, 480, 600, 580, 620, 650]
    
    return pd.DataFrame({
        'Fecha': dates,
        'Llamadas': values
    })

# Obtener datos
api_data = get_api_data()

# Encabezado del panel - más limpio y simple
st.markdown(f"""
<div class="panel-header">
    <div>
        <h1>Panel de API</h1>
        <p class="welcome-text">Bienvenido, <span class="email-highlight">{api_data['email']}</span></p>
    </div>
</div>
""", unsafe_allow_html=True)

# Optimización: Diseño de dos columnas más eficiente
col1, col2 = st.columns(2, gap="medium")

# Optimización: Columna 1 - API Key con menos elementos DOM
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">Tu API Key</h2>', unsafe_allow_html=True)
    
    # Contenedor de la API Key optimizado
    key_col, btn_col = st.columns([7, 3])
    with key_col:
        api_key = st.text_input("", value=api_data["api_key"], key="api_key_input", 
                               disabled=True, label_visibility="collapsed")
    with btn_col:
        copy_btn = st.button("Copiar", key="copy_button", use_container_width=True)
    
    # Advertencia simplificada
    st.markdown("""
    <div class="warning-text">
        <span class="warning-icon">⚠</span> No compartas esta clave
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de regenerar clave optimizado
    st.button("↻ Regenerar clave", key="regen_button", type="secondary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Optimización: Columna 2 - Uso de API más limpio
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-title">Uso de API</h2>', unsafe_allow_html=True)
    
    # Estadísticas más eficientes
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{api_data['api_calls_today']}</div>
            <div class="stat-label">Llamadas hoy</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{api_data['api_calls_month']}</div>
            <div class="stat-label">Este mes</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Uso del límite optimizado
    st.markdown(f"""
    <div class="stat-card" style="margin-top: 0.75rem;">
        <div class="stat-value">{api_data['usage_percentage']}%</div>
        <div class="stat-label">Del límite</div>
    </div>
    <div class="progress-container">
        <div class="progress-labels">
            <div>0</div>
            <div>{api_data['limit_per_day']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de progreso optimizada
    st.progress(api_data['usage_percentage']/100, "progress_bar")
    
    # Información del plan optimizada
    st.markdown(f"""
    <div class="plan-info">
        <div class="plan-name">{api_data['plan_name']}</div>
        <div class="plan-limit">Límite: {api_data['limit_per_day']:,} llamadas/día</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón actualizar plan
    st.button("↑ Actualizar plan", key="update_plan", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Optimización: Sección de documentación más ligera
st.markdown("""
<div class="card">
    <h2 class="doc-title">📚 Documentación API</h2>
    <p style="font-size: 0.9rem; margin-bottom: 1rem; color: #4b5563;">
        Accede a nuestra documentación completa para integrar la API en tus sistemas:
    </p>
""", unsafe_allow_html=True)

# Crear enlaces de documentación de forma más eficiente
doc_links = [
    {"icon": "📄", "text": "Guía de introducción"},
    {"icon": "</> ", "text": "Referencia de endpoints"},
    {"icon": "⬇ ", "text": "SDKs oficiales"},
    {"icon": "❓", "text": "Preguntas frecuentes"},
]

# Renderizar enlaces de forma más eficiente
doc_html = ""
for link in doc_links:
    doc_html += f"""
    <a href="#" class="doc-link">
        <span class="doc-link-icon">{link['icon']}</span> {link['text']}
    </a>
    """

st.markdown(doc_html + "</div>", unsafe_allow_html=True)

# Optimización: Botón para ver documentación completa renderizado de forma más eficiente
st.button("↗ Ver documentación completa", key="view_docs", type="secondary", use_container_width=False)

# Optimización: Gráfico de tendencia
st.markdown("<div class='card'><h3 style='font-size: 1rem; font-weight: 600; margin-bottom: 1rem;'>Tendencia de uso reciente</h3>", unsafe_allow_html=True)

# Optimización: Usar datos cacheados para el gráfico
chart_data = get_chart_data()

# Gráfico de línea optimizado
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=chart_data['Fecha'],
    y=chart_data['Llamadas'],
    mode='lines+markers',
    name='Llamadas API',
    line=dict(color='#3b82f6', width=2),
    marker=dict(size=6)
))

fig.update_layout(
    margin=dict(t=10, b=10, l=10, r=10),
    height=250,
    xaxis_title="",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(230,230,230,0.8)',
        zeroline=False
    ),
    hovermode='x unified'
)

# Renderizar gráfico de forma más eficiente
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
st.markdown("</div>", unsafe_allow_html=True)

# Funcionalidad para copiar al portapapeles
if "copied" not in st.session_state:
    st.session_state.copied = False

# Manejo del estado para la funcionalidad de copiar
if copy_btn:
    st.session_state.copied = True
    
# Mostrar mensaje de éxito cuando se copia
if st.session_state.copied:
    st.success("¡Clave copiada al portapapeles!")
    # Reiniciar el estado después de mostrar el mensaje
    st.session_state.copied = False