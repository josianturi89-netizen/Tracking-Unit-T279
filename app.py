import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga Bogor - Tracking Unit", layout="wide")

# 2. Sidebar - Judul Custom Warna
st.sidebar.markdown("""
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
        m1.metric("Pabrik (KARAWANG)", counts.get("TNVDC-KARAWANG", 0))
        m2.metric("Transit (CIBITUNG)", counts.get("TNVDC-CIBITUNG", 0))
        m3.metric("Ready (TPDC-CBN)", counts.get("TPDC-CBN", 0))
        
        st.markdown("---")

        # --- FITUR PENCARIAN & FILTER ---
        st.subheader("🔍 Pencarian & Monitoring Unit")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            search_cust = st.text_input("👤 Cari Nama Customer")
        with col_s2:
            search_sales = st.text_input("👔 Cari Nama Salesman")
        with col_s3:
            loc_options = ["Semua Lokasi"] + df['Func.Loc'].dropna().unique().tolist()
            filter_loc = st.selectbox("📍 Filter Lokasi", options=loc_options)

        # Logika Filtering
        mask = df['Customer Name'].str.contains(search_cust, case=False, na=False) & \
               df['Salesman Name'].str.contains(search_sales, case=False, na=False)
        
        if filter_loc != "Semua Lokasi":
            mask = mask & (df['Func.Loc'] == filter_loc)
            
        filtered_df = df[mask]

        # Menampilkan Tabel
        st.dataframe(
            filtered_df[['Customer Name', 'Salesman Name', 'Func.Loc', 'Age', 'Keterangan']],
            use_container_width=True,
            hide_index=True
        )

        # --- GRAFIK VISUAL ---
        st.markdown("---")
        order = ["TNVDC-KARAWANG", "TNVDC-CIBITUNG", "TPDC-CBN"]
        chart_data = df['Func.Loc'].value_counts().reindex(order).fillna(0).reset_index()
        chart_data.columns = ['Lokasi', 'Jumlah Unit']

        fig = px.bar(
            chart_data,
            x='Lokasi', y='Jumlah Unit', 
            color='Lokasi',
            text='Jumlah Unit',
            color_discrete_map={
                "TNVDC-KARAWANG": "#FF0000", 
                "TNVDC-CIBITUNG": "#FFAA00", 
                "TPDC-CBN": "#00CC96"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal membaca file. (Error: {e})")
else:
    st.warning("👈 Silakan upload file laporan AR Anda untuk memulai.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logo_Auto2000.png/640px-Logo_Auto2000.png", width=250)
