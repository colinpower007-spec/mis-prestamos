import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestor de Préstamos", layout="wide")

CLAVE_MAESTRA = "1234" 

if "autenticado" not in st.session_state:
    st.title("🔐 Acceso Privado")
    password = st.text_input("Introduce tu clave:", type="password")
    if password == CLAVE_MAESTRA:
        st.session_state["autenticado"] = True
        st.rerun()
else:
    # CONEXIÓN USANDO LOS SECRETS
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        # Lee la hoja configurada en los Secrets
        df = conn.read(ttl=0)
        
        st.title("💰 Mis Préstamos al 15% Mensual")

        st.subheader("➕ Registrar Nuevo Préstamo")
        with st.form("formulario", clear_on_submit=True):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre del Deudor")
            capital = col2.number_input("Monto ($)", min_value=0.0)
            if st.form_submit_button("🚀 GUARDAR"):
                if nombre and capital > 0:
                    nuevo = pd.DataFrame([{"Nombre": nombre, "Capital": capital, "Fecha": "Hoy"}])
                    df_act = pd.concat([df, nuevo], ignore_index=True)
                    conn.update(data=df_act)
                    st.success("¡Datos guardados!")
                    st.rerun()

        if not df.empty:
            df['Capital'] = pd.to_numeric(df['Capital'], errors='coerce').fillna(0)
            df['Interés'] = df['Capital'] * 0.15
            df['Total'] = df['Capital'] + df['Interés']
            
            st.metric("Total en Calle", f"${df['Total'].sum():,.2f}")
            st.dataframe(df, use_container_width=True)
            st.plotly_chart(px.pie(df, values='Capital', names='Nombre'))
    except Exception as e:
        st.error("Error: Configura el enlace en 'Settings > Secrets' de Streamlit Cloud.")
        st.write(e)
