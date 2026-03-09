import streamlit as st
import pandas as pd
import plotly.express as px

# --- SEGURIDAD ---
CLAVE_MAESTRA = "1234" 

if "autenticado" not in st.session_state:
    st.title("🔐 Acceso")
    password = st.text_input("Clave:", type="password")
    if password == CLAVE_MAESTRA:
        st.session_state["autenticado"] = True
        st.rerun()
else:
    st.title("💰 Mis Préstamos al 15%")
    
    # Datos de ejemplo
    if 'datos' not in st.session_state:
        st.session_state.datos = pd.DataFrame(
            [{'Nombre': 'Ejemplo', 'Capital': 1000.0}]
        )

    df = st.session_state.datos
    df['Interés (15%)'] = df['Capital'] * 0.15
    df['Monto Total'] = df['Capital'] + df['Interés (15%)']

    # Métricas
    st.metric("Total Capital", f"${df['Capital'].sum():,.2f}")
    
    # Tabla
    st.subheader("📋 Listado")
    st.table(df)

    # Gráfico
    fig = px.pie(df, values='Capital', names='Nombre')
    st.plotly_chart(fig)
