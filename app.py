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
    st.title("💰 Mis Préstamos al 15% Mensual")
    
    # Intentar conexión
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        
        # Formulario
        with st.expander("➕ Registrar Nuevo Préstamo", expanded=True):
            with st.form("formulario", clear_on_submit=True):
                nombre = st.text_input("Nombre")
                capital = st.number_input("Monto", min_value=0.0)
                if st.form_submit_button("🚀 GUARDAR"):
                    if nombre and capital > 0:
                        nuevo = pd.DataFrame([{"Nombre": nombre, "Capital": capital, "Fecha": "Hoy"}])
                        df_act = pd.concat([df, nuevo], ignore_index=True)
                        conn.update(data=df_act)
                        st.cache_data.clear()
                        st.success("¡Datos guardados!")
                        st.rerun()

        if not df.empty:
            df['Capital'] = pd.to_numeric(df['Capital'], errors='coerce').fillna(0)
            st.metric("Total Capital", f"${df['Capital'].sum():,.2f}")
            st.dataframe(df, use_container_width=True)
            st.plotly_chart(px.pie(df, values='Capital', names='Nombre'))

    except Exception as e:
        st.error("Error de conexión. Asegúrate de que la hoja sea PÚBLICA y EDITABLE.")
        st.info("Revisa 'Settings > Secrets' en Streamlit Cloud.")
        if st.button("🔄 Reintentar conexión"):
            st.cache_data.clear()
            st.rerun()
