import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# State & Konfigurasi CSS
if 'theme' not in st.session_state: st.session_state.theme = 'Dark'
theme_mode = st.sidebar.radio("🎨 Pilih Mode Tampilan:", ['Dark', 'White'], index=0 if st.session_state.theme == 'Dark' else 1)
st.session_state.theme = theme_mode

bg_color, text_color, card_bg = ("#0e1117", "#ffffff", "#1c2128") if st.session_state.theme == 'Dark' else ("#ffffff", "#000000", "#f0f2f6")
header_color = "#e60012"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .brand-box {{ background-color: {header_color}; color: white; padding: 25px; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1.5em; margin-bottom: 25px; }}
    .metric-card {{ background-color: {card_bg}; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }}
    .customer-name {{ font-weight: bold; color: {'#e60012' if st.session_state.theme == 'White' else '#58a6ff'}; }}
    .sales-name {{ font-size: 0.85em; color: #8b949e; }}
    thead tr th {{ background-color: {header_color} !important; color: white !important; text-align: center !important; }}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    # Membaca data dengan header 2 baris
    df = pd.read_excel(uploaded_file, header=[0, 1])
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

    # Urutan lokasi agar rapi (Unknown ditaruh di akhir)
    order_map = {'TNVDC-KARAWANG': 1, 'TNVDC-CIBITUNG': 2, 'TPDC-CBN': 3, 'TCUST': 4}
    df['Urutan'] = df['Posisi'].map(order_map).fillna(5)
    df = df.sort_values('Urutan')

    # Filter Salesman
    sales_list = ["Semua Salesman"] + sorted(df[cols_sales].dropna().unique().tolist())
    sales_search = st.selectbox("👔 Filter Salesman", options=sales_list)
    f_df = df[df[cols_sales] == sales_search] if sales_search != "Semua Salesman" else df

    # Metric Cards Dinamis
    unique_locs = f_df['Posisi'].unique()
    cols = st.columns(len(unique_locs) if len(unique_locs) > 0 else 1)
    for i, loc in enumerate(unique_locs):
        count = len(f_df[f_df.Posisi == loc])
        cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{count}</h2></div>', unsafe_allow_html=True)

    # Tabel Utama
    st.markdown("### 📋 Detail Status Unit")
    display_df = f_df.copy()
    
    # Format Customer & Salesman (HTML)
    display_df['Customer & Salesman'] = display_df.apply(
        lambda x: f'<div class="customer-name">{x[cols_cust]}</div><div class="sales-name">👤 {x[cols_sales]}</div>', axis=1
    )
    
    # PERUBAHAN: Mengatur urutan kolom agar 'Posisi' berada di paling kanan
    display_df = display_df[['Customer & Salesman', cols_equip, cols_detail, 'Posisi']]
    display_df = display_df.rename(columns={cols_equip: 'No. Rangka', cols_detail: 'Detail'})
    
    # Tampilkan Tabel
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("👈 Silakan upload file Excel untuk memulai.")
