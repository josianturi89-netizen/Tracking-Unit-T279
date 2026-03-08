import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# CSS untuk desain modern
header_color = "#e60012"
st.markdown(f"""
    <style>
    .brand-box {{ background-color: {header_color}; color: white; padding: 25px; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1.5em; margin-bottom: 25px; }}
    .metric-card {{ background-color: #1c2128; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }}
    thead tr th {{ background-color: {header_color} !important; color: white !important; }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    # Membaca data dengan header 2 baris
    df = pd.read_excel(uploaded_file, header=[0, 1])
    
    # Menyamakan format kolom menjadi satu baris (menghilangkan _nan)
    df.columns = [f"{a}_{b}".replace('_nan', '').strip() for a, b in df.columns]
    
    # Mengidentifikasi kolom secara dinamis
    cols_cust = [c for c in df.columns if 'Customer Name' in c][0]
    cols_sales = [c for c in df.columns if 'Salesman Name' in c][0]
    cols_equip = [c for c in df.columns if 'Equipment' in c][0]
    cols_detail = [c for c in df.columns if 'Detail' in c][0]
    func_cols = [c for c in df.columns if 'Func.Loc' in c]
    
    # Fungsi menentukan posisi
    def get_posisi(row):
        for col in func_cols:
            if pd.notna(row[col]): return str(row[col])
        return "Unknown"
    
    df['Posisi'] = df.apply(get_posisi, axis=1)
    
    # Urutan lokasi (untuk sorting metrik dan tabel)
    order_map = {'TNVDC-KARAWANG': 1, 'TNVDC-CIBITUNG': 2, 'TPDC-CBN': 3, 'TCUST': 4}
    df['Urutan'] = df['Posisi'].map(order_map).fillna(5)
    df = df.sort_values('Urutan')
    
    # Metric Cards
    locs = ['TNVDC-KARAWANG', 'TNVDC-CIBITUNG', 'TPDC-CBN', 'TCUST']
    cols = st.columns(4)
    for i, loc in enumerate(locs):
        count = len(df[df.Posisi == loc])
        cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{count}</h2></div>', unsafe_allow_html=True)
    
    # Tabel Utama (Langsung tampilkan data dari kolom yang ditemukan)
    st.markdown("### 📋 Detail Status Unit")
    st.write(df[[cols_cust, cols_sales, cols_equip, 'Posisi', cols_detail]].to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("👈 Silakan upload file Excel untuk memulai.")
