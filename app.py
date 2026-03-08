import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga Bogor - Tracking Unit", layout="wide")

# 2. Sidebar - Judul Custom Warna
st.sidebar.markdown(f"""
    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333;">
        <h1 style="color: #FF0000; margin-bottom: 0; font-family: sans-serif; font-weight: bold;">Auto2000</h1>
        <h3 style="color: #FFFFFF; margin-top: 0; font-family: sans-serif;">Dramaga Bogor</h3>
        <hr style="border-color: #444;">
    </div>
    <br>
    """, unsafe_allow_html=True)

st.sidebar.header("📁 Update Data AR")
uploaded_file = st.sidebar.file_uploader("Upload file Excel/CSV di sini", type=["xlsx", "xls", "csv"])

# 3. Konten Utama
st.title("🚗 Dashboard Monitoring Logistik Unit")
st.markdown("---")

if uploaded_file is not None:
    try:
        # Membaca data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # --- METRIC SUMMARY ---
        counts = df['Func.Loc'].value_counts()
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Pabrik (KARAWANG)", counts.get("TNVDC-KARAWANG", 0))
        with m2:
            st.metric("Transit (CIBITUNG)", counts.get("TNVDC-CIBITUNG", 0))
        with m
