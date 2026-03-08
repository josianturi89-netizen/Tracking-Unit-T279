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
    thead tr th {{ background-color: {header_color} !important; color: white !important; text-align: center !important; }}
    .customer-name {{ font-weight: bold; color: #58a6ff; }}
    .sales-name {{ font-size: 0.85em; color: #8b949e; }}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE, header=[0, 1])
    return None

tab_monitor, tab_admin = st.tabs(["📊 Dashboard Monitoring", "⚙️ Admin & Upload"])

with tab_admin:
    st.subheader("Manajemen Data Unit")
    uploaded_file = st.file_uploader("Upload file Excel terbaru", type=["xlsx", "csv"])
    if uploaded_file:
        with open(DATA_FILE, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Data berhasil diperbarui!")

with tab_monitor:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h2 style="color: white; font-weight: bold; margin-bottom: 5px;">Dashboard Monitoring Unit TSO-Dramaga Bogor</h2>
            <p style="color: white; opacity: 0.7; font-size: 0.9em; font-style: italic;">For Internal Condition Auto2000 Dramaga Bogor Only</p>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    
    if df is not None:
        df.columns = [f"{a}_{b}".replace('_nan', '').strip() for a, b in df.columns]
        
        # Identifikasi kolom
        cols_cust = [c for c in df.columns if 'Customer Name' in c][0]
        cols_sales = [c for c in df.columns if 'Salesman Name' in c][0]
        cols_equip = [c for c in df.columns if 'Equipment' in c][0]
        cols_detail = [c for c in df.columns if 'Detail' in c][0]
        cols_status = [c for c in df.columns if 'Status Kirim' in c][0]
        func_cols = [c for c in df.columns if 'Func.Loc' in c]
        
        df['Posisi'] = df.apply(lambda row: next((row[c] for c in func_cols if pd.notna(row[c])), "Unknown"), axis=1)
        
        # Logika Status Pembayaran (Kolom Baru)
        def cek_pembayaran(val):
            return "✅" if str(val).strip() in ["Lunas DP", "Lunas AR"] else "➖"
        
        df['Status Pembayaran'] = df[cols_detail].apply(cek_pembayaran)
        
        # Sortir
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
            cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{len(f_df[f_df.Posisi == loc])}</h2></div>', unsafe_allow_html=True)
            
        # Tabel
        st.markdown("### 📋 Detail Status Unit")
        display_df = f_df.copy()
        display_df['Customer & Salesman'] = display_df.apply(lambda x: f'<div class="customer-name">{x[cols_cust]}</div><div class="sales-name">👤 {x[cols_sales]}</div>', axis=1)
        
        # Urutan Kolom Final
        final_df = display_df[['Customer & Salesman', cols_equip, cols_detail, 'Status Pembayaran', cols_status, 'Posisi']]
        final_df = final_df.rename(columns={cols_equip: 'No. Rangka', cols_detail: 'Detail', cols_status: 'Status Kirim'})
        
        st.write(final_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("Belum ada data. Silakan upload file di tab 'Admin & Upload'.")
