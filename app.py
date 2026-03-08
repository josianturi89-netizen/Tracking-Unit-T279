import streamlit as st
import pandas as pd
import plotly.express as px

# Set tampilan dashboard
st.set_page_config(page_title="Dashboard Tracking Unit", layout="wide")

st.title("🚗 Dashboard Monitoring Logistik Unit")
st.markdown("---")

# Fitur Upload di Sidebar
st.sidebar.header("Konfigurasi Data")
uploaded_file = st.sidebar.file_uploader("Upload File Excel atau CSV", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    # Proses pembacaan file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # --- BAGIAN VISUAL UTAMA (PIPELINE) ---
        st.subheader("📊 Ringkasan Alur Unit (Func. Loc)")
        
        # Definisikan urutan flow sesuai permintaan user
        order = ["TNVDC-KARAWANG", "TNVDC-CIBITUNG", "TPDC-CBN"]
        
        # Hitung jumlah unit per lokasi
        counts = df['Func.Loc'].value_counts()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("1. KARAWANG (Pabrik)", counts.get("TNVDC-KARAWANG", 0))
        m2.metric("2. CIBITUNG (Transit)", counts.get("TNVDC-CIBITUNG", 0))
        m3.metric("3. CBN (Ready Delivery)", counts.get("TPDC-CBN", 0))
        
        st.markdown("---")

        # --- FITUR SEARCH & FILTER ---
        st.subheader("🔍 Monitoring & Pencarian Unit")
        
        # Kolom pencarian interaktif
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            search_cust = st.text_input("Cari Nama Customer")
        with col_s2:
            search_sales = st.text_input("Cari Nama Salesman")
        with col_s3:
            filter_loc = st.multiselect("Filter Lokasi", options=df['Func.Loc'].unique().tolist())

        # Logika Filtering
        mask = df['Customer Name'].str.contains(search_cust, case=False, na=False) & \
               df['Salesman Name'].str.contains(search_sales, case=False, na=False)
        
        if filter_loc:
            mask = mask & df['Func.Loc'].isin(filter_loc)
            
        filtered_df = df[mask]

        # Tampilkan Tabel
        st.dataframe(
            filtered_df[['Customer Name', 'Salesman Name', 'Func.Loc', 'Age', 'Keterangan']],
            use_container_width=True,
            hide_index=True
        )

        # Chart Distribusi
        st.markdown("---")
        fig = px.bar(
            df['Func.Loc'].value_counts().reindex(order).reset_index(),
            x='Func.Loc', y='count', 
            title="Posisi Unit dalam Supply Chain",
            color='Func.Loc',
            color_discrete_map={"TNVDC-KARAWANG":"#FF4B4B", "TNVDC-CIBITUNG":"#FFAA00", "TPDC-CBN":"#00CC96"}
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: Pastikan format kolom Excel sesuai. Detail: {e}")
else:
    st.warning("👈 Silakan upload file Excel/CSV Anda pada menu di samping kiri untuk melihat dashboard.")
    st.info("Catatan: Pastikan file memiliki kolom: 'Customer Name', 'Salesman Name', 'Func.Loc', 'Age', 'Keterangan'")
