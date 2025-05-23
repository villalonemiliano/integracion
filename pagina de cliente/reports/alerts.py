import streamlit as st

# Set page config
st.set_page_config(layout="wide")

# Apply custom CSS for styling
st.markdown("""
<style>
    .main-container {
        background-color: #f9f9f9;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .header-container {
        text-align: center;
        padding: 2rem 0;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .header-title span {
        color: #3366FF;
        border-bottom: 3px solid #3366FF;
        padding-bottom: 0.2rem;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #555;
        margin: 0.5rem 0 2rem 0;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }
    .features-container {
        display: flex;
        justify-content: space-between;
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .feature-card {
        background-color: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        flex: 1;
    }
    .feature-icon {
        background-color: #EAEFFF;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    .feature-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #333;
    }
    .feature-description {
        color: #666;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    .feature-link {
        color: #3366FF;
        text-decoration: none;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .icon-bolt { content: "⚡"; }
    .icon-fire { content: "🔍"; }
    .icon-info { content: "📊"; }
    
    /* For mobile responsiveness */
    @media (max-width: 768px) {
        .features-container {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header Section
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Nuestro <span>Algoritmo</span></h1>
        <p class="header-subtitle">Tecnología avanzada para análisis de mercado preciso</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns using streamlit's columns layout
    col1, col2, col3 = st.columns(3)
    
    # Feature 1
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <span class="icon-bolt" style="font-size: 24px;">⚡</span>
            </div>
            <h3 class="feature-title">Recolección de datos en tiempo real</h3>
            <p class="feature-description">
                Nuestros nodos distribuidos capturan datos de 27 mercados globales con latencia
                menor a 50ms. Incluye precios, volumen y datos fundamentales.
            </p>
            <a href="#" class="feature-link">Más información →</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 2
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <span class="icon-fire" style="font-size: 24px;">🔍</span>
            </div>
            <h3 class="feature-title">Análisis técnico multicapa</h3>
            <p class="feature-description">
                Evaluamos simultáneamente 14 indicadores técnicos con ponderaciones
                dinámicas que se ajustan a las condiciones del mercado.
            </p>
            <a href="#" class="feature-link">Más información →</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 3
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <span class="icon-info" style="font-size: 24px;">📊</span>
            </div>
            <h3 class="feature-title">Procesamiento de alto rendimiento</h3>
            <p class="feature-description">
                Nuestra arquitectura distribuida procesa millones de puntos de datos por segundo para
                entregar resultados en tiempo real.
            </p>
            <a href="#" class="feature-link">Más información →</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)