import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# State untuk tema
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

theme_mode = st.sidebar.radio("🎨 Pilih Mode Tampilan:", ['Dark', 'White'], index=0 if st.session_state.theme == 'Dark' else 1)
st.session_state.theme = theme_mode

# Konfigurasi CSS
bg_color, text_color, card_bg = ("#0e1117", "#ffffff", "#1c2128") if st.session_state.theme == 'Dark' else ("#ffffff", "#000000", "#f0f2f6")
header_color = "#e60012"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .brand-box {{ background-color: {header_color}; color: white; padding: 25px; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1.5em; margin-bottom: 25px; }}
    .metric-card {{ background-color: {card_bg}; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }}
    thead tr th {{ background-color: {header_color} !important; color: white !important; text-align: center !important; }}
    .customer-name {{ font-weight: bold; color: {'#e60012' if st.session_state.theme == 'White' else '#58a6ff'}; }}
    .sales-name {{ font-size: 0.85em; color: #8b949e; }}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    # Membaca header dua baris
    df = pd.read_excel(uploaded_file, header=[0, 1])
    
    # Flatten header (menggabungkan baris 1 dan 2)
    df.columns = [f"{a}_{b}".replace("_nan", "").strip() for a, b in df.columns]
    
    # Menemukan kolom Func.Loc
    func_cols = [c for c in df.columns if 'Func.Loc' in c]
    
    # Logika menggabungkan 4 kolom lokasi menjadi 1
    def get_posisi(row):
        for col in func_cols:
            if pd.notna(row[col]): return row[col]
        return "Unknown"

    df['Posisi'] = df.apply(get_posisi, axis=1)
    
    # Filter Salesman (mengambil kolom yang tepat)
    sales_col = [c for c in df.columns if 'Salesman Name' in c][0]
    cust_col = [c for c in df.columns if 'Customer Name' in c][0]
    equip_col = [c for c in df.columns if 'Equipment' in c][0]
    detail_col = [c for c in df.columns if 'Detail' in c][0]
    
    sales_list = ["Semua Salesman"] + sorted(df[sales_col].dropna().unique().tolist())
    sales_search = st.selectbox("👔 Filter Salesman", options=sales_list)
    
    f_df = df[df[sales_col] == sales_search] if sales_search != "Semua Salesman" else df

    # Metric Cards (Dinamis sesuai data)
    locs = f_df['Posisi'].unique()
    cols = st.columns(len(locs) if len(locs) > 0 else 1)
    for i, loc in enumerate(locs):
        count = len(f_df[f_df.Posisi == loc])
        cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{count}</h2></div>', unsafe_allow_html=True)

    # Tabel Utama
    st.markdown("### 📋 Detail Status Unit")
    display_df = f_df.copy()
    display_df['Customer & Salesman'] = display_df.apply(
        lambda x: f'<div class="customer-name">{x[cust_col]}</div><div class="sales-name">👤 {x[sales_col]}</div>', axis=1
    )
    
    st.write(display_df[['Posisi', 'Customer & Salesman', equip_col, detail_col]]
             .rename(columns={equip_col: 'No. Rangka', detail_col: 'Detail'})
             .to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("👈 Silakan upload file Excel untuk memulai.")
