import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestor de Préstamos", layout="wide")

# --- SEGURIDAD ---
if "autenticado" not in st.session_state:
    st.title("🔐 Acceso")
    pwd = st.text_input("Clave:", type="password")
    if pwd == "1234":
        st.session_state["autenticado"] = True
        st.rerun()
else:
    st.title("💰 Mis Préstamos al 15%")
    
    # ID de tu hoja de Google
    SHEET_ID = "1k--H7hA036VsxpJy2lpeit37IISXauM_drsFYMawkEs"
    URL_CSV = f"https://docs.google.com{SHEET_ID}/export?format=csv"
    
    try:
        # Lectura directa
        df = pd.read_csv(URL_CSV)
        df.columns = [c.strip() for c in df.columns]

        # Métricas y Cálculos
        if not df.empty and 'Capital' in df.columns:
            df['Capital'] = pd.to_numeric(df['Capital'], errors='coerce').fillna(0)
            df['Interés (15%)'] = df['Capital'] * 0.15
            df['Total'] = df['Capital'] + df['Interés (15%)']
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Capital Prestado", f"${df['Capital'].sum():,.2f}")
            c2.metric("Intereses (15%)", f"${df['Interés (15%)'].sum():,.2f}")
            c3.metric("Total a Cobrar", f"${df['Total'].sum():,.2f}")
            
            st.subheader("📋 Detalle de Deudores")
            st.dataframe(df, use_container_width=True)
            
            st.subheader("📊 Gráfico de Distribución")
            st.plotly_chart(px.pie(df, values='Capital', names='Nombre', hole=0.3))
        
        st.divider()
        st.info("💡 Para agregar o quitar deudores, edita tu Google Sheet:")
        st.link_button("📝 Abrir Google Sheets", f"https://docs.google.com{SHEET_ID}/edit")

    except Exception as e:
        st.error("Error al leer los datos.")
        st.write("Asegúrate de que la hoja esté 'Publicada en la Web' (Archivo > Compartir > Publicar en la Web).")
