import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# Konfigurasi Path Penyimpanan
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "latest_data.xlsx")
os.makedirs(DATA_DIR, exist_ok=True)

# CSS Kustom
header_color = "#e60012"
st.markdown(f"""
    <style>
    .brand-box {{ background-color: {header_color}; color: white; padding: 20px; border-radius: 10px; text-align: center; font-weight: 900; }}
    .metric-card {{ background-color: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; text-align: center; }}
    thead tr th {{ background-color: {header_color} !important; color: white !important; }}
    .customer-name {{ font-weight: bold; color: #58a6ff; }}
    .sales-name {{ font-size: 0.85em; color: #8b949e; }}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)

# Tab Utama
tab_monitor, tab_admin = st.tabs(["📊 Dashboard Monitoring", "⚙️ Admin & Upload"])

# Fungsi untuk memuat data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE, header=[0, 1])
    return None

# --- TAB ADMIN ---
with tab_admin:
    st.subheader("Manajemen Data Unit")
    uploaded_file = st.file_uploader("Upload file Excel terbaru", type=["xlsx", "csv"])
    if uploaded_file:
        with open(DATA_FILE, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Data berhasil diperbarui!")

# --- TAB MONITORING ---
with tab_monitor:
    df = load_data()
    
    if df is not None:
        # Pembersihan Nama Kolom
        df.columns = [f"{a}_{b}".replace('_nan', '').strip() for a, b in df.columns]
        
        # Identifikasi kolom dinamis
        cols_cust = [c for c in df.columns if 'Customer Name' in c][0]
        cols_sales = [c for c in df.columns if 'Salesman Name' in c][0]
        cols_equip = [c for c in df.columns if 'Equipment' in c][0]
        cols_detail = [c for c in df.columns if 'Detail' in c][0]
        func_cols = [c for c in df.columns if 'Func.Loc' in c]
        
        def get_posisi(row):
            for col in func_cols:
                if pd.notna(row[col]): return str(row[col])
            return "Unknown"
        
        df['Posisi'] = df.apply(get_posisi, axis=1)
        
        # Sortir Berdasarkan Urutan
        order_map = {'TNVDC-KARAWANG': 1, 'TNVDC-CIBITUNG': 2, 'TPDC-CBN': 3, 'TCUST': 4}
        df['Urutan'] = df['Posisi'].map(order_map).fillna(5)
        df = df.sort_values('Urutan')
        
        # Filter Salesman
        sales_list = ["Semua Salesman"] + sorted(df[cols_sales].dropna().unique().tolist())
        selected_sales = st.selectbox("👔 Filter Salesman", sales_list)
        f_df = df[df[cols_sales] == selected_sales] if selected_sales != "Semua Salesman" else df
        
        # Metric Cards
        cols = st.columns(4)
        labels = ['TNVDC-KARAWANG', 'TNVDC-CIBITUNG', 'TPDC-CBN', 'TCUST']
        for i, loc in enumerate(labels):
            count = len(f_df[f_df.Posisi == loc])
            cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{count}</h2></div>', unsafe_allow_html=True)
            
        # Tabel Utama (Posisi di kanan)
        st.markdown("### 📋 Detail Status Unit")
        display_df = f_df.copy()
        display_df['Customer & Salesman'] = display_df.apply(
            lambda x: f'<div class="customer-name">{x[cols_cust]}</div><div class="sales-name">👤 {x[cols_sales]}</div>', axis=1
        )
        final_df = display_df[['Customer & Salesman', cols_equip, cols_detail, 'Posisi']]
        final_df = final_df.rename(columns={cols_equip: 'No. Rangka', cols_detail: 'Detail'})
        
        st.write(final_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
    else:
        st.info("Belum ada data. Silakan upload file di tab 'Admin & Upload'.")
