import streamlit as st
from send_email import send

to = "contacto@tonidev.es"
sender = "Tool"
subject = "Reporte de errores Gestoria VilaFant"

st.title("Algo que nos quieras comentar?")

st.markdown("Rellena este cuestionario para ponerte en contacto con nosotros para razones de soporte.")

# Formulario para reportar errores
with st.form(key="error_report"):
    descripcion = st.text_area("Descripción del soporte necesario")
    pasos = st.text_area("Nombre de cliente y correo electronico.")
    comentarios  = st.text_area("Comentarios adicionales (opcional)")
    file = st.file_uploader("Adjuntar captura de pantalla (opcional)", type=["png", "jpg", "jpeg"])
    # Enviar formulario
    if st.form_submit_button("Enviar reporte"):
        st.spinner("Enviando reporte...")
        # Lógica de envío de correo
        send(descripcion,pasos,descripcion,to,file,)
        st.success("¡Gracias por tu comentario!")