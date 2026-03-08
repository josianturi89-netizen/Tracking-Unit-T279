import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga - Sales Dashboard", layout="wide")

# 2. Sidebar Branding
st.sidebar.markdown("""
    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333;">
        <h1 style="color: #FF0000; margin-bottom: 0; font-weight: bold;">Auto2000</h1>
        <h3 style="color: #FFFFFF; margin-top: 0;">Dramaga Bogor</h3>
        <p style="color: #aaa; font-size: 0.8rem;">Admin Support for Salesman</p>
        <hr style="border-color: #444;">
    </div>
    <br>
    """, unsafe_allow_html=True)

st.sidebar.header("📁 Upload Database AR")
uploaded_file = st.sidebar.file_uploader("Upload File Excel/CSV", type=["xlsx", "xls", "csv"])

# 3. Konten Utama
st.title("🚛 Dashboard Monitoring Delivery Unit")
st.markdown("Dashboard ini melacak unit berdasarkan kata kunci lokasi (Karawang, Cibitung, atau CBN).")

if uploaded_file is not None:
    try:
        # Membaca data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # --- DATA CLEANING & SMART MAPPING ---
        # 1. Leasing Name: Isi kosong dengan 'Tunai'
        if 'Leasing Name' in df.columns:
            df['Leasing Name'] = df['Leasing Name'].fillna('Tunai')
        
        # 2. Billing Date: Post Date -> Date Format
        if 'Post Date' in df.columns:
            df['Billing Date'] = pd.to_datetime(df['Post Date'], errors='coerce').dt.strftime('%d-%m-%Y')

        # 3. Smart Func.Loc Mapping (Mencari keyword)
        def map_location(loc):
            loc = str(loc).upper()
            if "CBN" in loc:
                return "READY (CBN)"
            elif "CIBITUNG" in loc:
                return "TRANSIT (CIBITUNG)"
            elif "KARAWANG" in loc:
                return "PABRIK (KARAWANG)"
            else:
                return "LAINNYA / PROSES"

        df['Status Unit'] = df['Func.Loc'].apply(map_location)

        # --- FILTERING ---
        st.subheader("🔍 Cari Data Unit")
        c1, c2 = st.columns(2)
        with c1:
            sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist())
            sales_search = st.selectbox("Pilih Nama Salesman", options=sales_list)
        with c2:
            cust_search = st.text_input("Cari Nama Customer")

        # Logika Filter
        mask = df['Customer Name'].str.contains(cust_search, case=False, na=False)
        if sales_search != "Semua Salesman":
            mask = mask & (df['Salesman Name'] == sales_search)
        
        filtered_df = df[mask]

        # --- VISUALISASI PIPELINE ---
        st.markdown("---")
        
        # Hitung berdasarkan kategori baru
        total_karawang = filtered_df[filtered_df['Status Unit'] == "PABRIK (KARAWANG)"].shape[0]
        total_cibitung = filtered_df[filtered_df['Status Unit'] == "TRANSIT (CIBITUNG)"].shape[0]
        total_cbn = filtered_df[filtered_df['Status Unit'] == "READY (CBN)"].shape[0]

        m1, m2, m3 = st.columns(3)
        m1.metric("1. PABRIK (KARAWANG)", total_karawang)
        m2.metric("2. TRANSIT (CIBITUNG)", total_cibitung)
        m3.metric("3. READY (CBN)", total_cbn, delta="SIAP KIRIM" if total_cbn > 0 else None)

        # --- TABEL DETAIL ---
        st.markdown("---")
        st.subheader("📋 Detail Unit untuk Salesman")
        
        # Menggunakan kolom yang sudah dipetakan
        display_df = filtered_df[[
            'Salesman Name', 'Customer Name', 'Leasing Name', 
            'Equipment', 'Billing No', 'Billing Date', 'Status Unit', 'Keterangan'
        ]].rename(columns={'Equipment': 'No. Rangka', 'Status Unit': 'Posisi Unit Saat Ini'})
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Gagal memproses file. Pastikan kolom sesuai. Detail: {e}")
else:
    st.info("👈 Menunggu Admin mengunggah file Excel terbaru.")
