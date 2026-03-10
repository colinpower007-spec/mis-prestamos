import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestor de Préstamos", layout="wide")

if "autenticado" not in st.session_state:
    st.title("🔐 Acceso")
    pwd = st.text_input("Clave:", type="password")
    if pwd == "1234":
        st.session_state["autenticado"] = True
        st.rerun()
else:
    st.title("💰 Mis Préstamos al 15%")
    
    # URL CORREGIDA CON EL CAMINO COMPLETO (IMPORTANTE)
    ID = "1k--H7hA036VsxpJy2lpeit37IISXauM_drsFYMawkEs"
    URL = f"https://docs.google.com{ID}/gviz/tq?tqx=out:csv"
    
    try:
        # Lectura directa desde Google Sheets como CSV
        df = pd.read_csv(URL)
        df.columns = [str(c).strip() for c in df.columns]

        if not df.empty and 'Capital' in df.columns:
            # Asegurar que los datos sean números
            df['Capital'] = pd.to_numeric(df['Capital'], errors='coerce').fillna(0)
            df['Interés'] = df['Capital'] * 0.15
            df['Total'] = df['Capital'] + df['Interés']
            
            # Métricas superiores
            c1, c2, c3 = st.columns(3)
            c1.metric("Capital en Calle", f"${df['Capital'].sum():,.2f}")
            c2.metric("Intereses (15%)", f"${df['Interés'].sum():,.2f}")
            c3.metric("Monto Total", f"${df['Total'].sum():,.2f}")
            
            # Tabla de datos
            st.subheader("📋 Tabla de Deudores")
            st.dataframe(df, use_container_width=True)
            
            # Gráfico circular
            st.subheader("📊 Gráfico de Capital")
            fig = px.pie(df, values='Capital', names='Nombre', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Asegúrate de que tu Google Sheet tenga los títulos 'Nombre' y 'Capital' en la primera fila (A1 y B1).")
            st.write("Columnas detectadas en la hoja:", df.columns.tolist())

    except Exception as e:
        st.error("❌ Error de conexión con Google Sheets.")
        st.write("Verifica que la hoja esté configurada como 'Cualquier persona con el enlace' -> 'Editor'.")
        st.info(f"Detalle técnico: {e}")
