import streamlit as st
from streamlit_gsheets import GSheetsConnection
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
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        
        st.title("💰 Mis Préstamos")
        
        with st.form("nuevo"):
            nom = st.text_input("Nombre")
            cap = st.number_input("Monto", min_value=0.0)
            if st.form_submit_button("Guardar"):
                if nom and cap > 0:
                    nuevo = pd.DataFrame([{"Nombre": nom, "Capital": cap, "Fecha": "Hoy"}])
                    df_act = pd.concat([df, nuevo], ignore_index=True)
                    conn.update(data=df_act)
                    st.success("¡Guardado!")
                    st.rerun()

        if not df.empty:
            # Cálculos rápidos
            df['Capital'] = pd.to_numeric(df['Capital'], errors='coerce').fillna(0)
            df['Interés (15%)'] = df['Capital'] * 0.15
            df['Total'] = df['Capital'] + df['Interés (15%)']
            
            c1, c2 = st.columns(2)
            c1.metric("Capital en Calle", f"${df['Capital'].sum():,.2f}")
            c2.metric("Intereses Totales", f"${df['Interés (15%)'].sum():,.2f}")
            
            st.dataframe(df, use_container_width=True)
            st.plotly_chart(px.pie(df, values='Capital', names='Nombre'))
    except Exception as e:
        st.error("Error de conexión. Revisa los 'Secrets' en la web de Streamlit.")
        st.write(e)
