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
    URL_HOJA = "https://docs.google.com"
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL_HOJA, ttl=0)

    st.title("💰 Mis Préstamos al 15% Mensual")

    # --- FORMULARIO EN EL CENTRO (Más fácil de ver) ---
    st.subheader("➕ Registrar Nuevo Préstamo")
    with st.form("formulario", clear_on_submit=True):
        col_nom, col_cap, col_fec = st.columns(3)
        with col_nom:
            nombre = st.text_input("Nombre del Deudor")
        with col_cap:
            capital = st.number_input("Capital Prestado ($)", min_value=0.0, step=10.0)
        with col_fec:
            fecha = st.date_input("Fecha")
        
        enviar = st.form_submit_button("🚀 GUARDAR EN LA NUBE")

        if enviar and nombre:
            nuevo_dato = pd.DataFrame([{"Nombre": nombre, "Capital": capital, "Fecha": str(fecha)}])
            df_actualizado = pd.concat([df, nuevo_dato], ignore_index=True)
            conn.update(spreadsheet=URL_HOJA, data=df_actualizado)
            st.success(f"✅ ¡{nombre} registrado con éxito!")
            st.rerun()

    # --- VISUALIZACIÓN ---
    if not df.empty:
        df['Capital'] = pd.to_numeric(df['Capital'], errors='coerce').fillna(0)
        df['Interés (15%)'] = df['Capital'] * 0.15
        df['Total a Cobrar'] = df['Capital'] + df['Interés (15%)']

        c1, c2, c3 = st.columns(3)
        c1.metric("Capital Total", f"${df['Capital'].sum():,.2f}")
        c2.metric("Intereses Totales", f"${df['Interés (15%)'].sum():,.2f}")
        c3.metric("Monto en Calle", f"${df['Total a Cobrar'].sum():,.2f}")

        st.subheader("📋 Listado de Deudores")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Gráfico de Capital")
        fig = px.pie(df, values='Capital', names='Nombre', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
