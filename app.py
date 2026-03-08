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
    .loc-badge {{ font-size: 0.8em; font-weight: bold; padding: 2px 8px; border-radius: 10px; background: {header_color}; color: white; }}
    thead tr th {{ background-color: {header_color} !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=[0, 1])
    df.columns = [f"{a}_{b}".replace("_nan", "").strip() for a, b in df.columns]
    
    # 1. Definisikan urutan pergerakan (Sesuai permintaan Anda)
    order_map = {
        'TNVDC-KARAWANG': 1,
        'TNVDC-CIBITUNG': 2,
        'TPDC-CBN': 3,
        'TCUST': 4
    }
    
    # 2. Ambil data Func.Loc dan mapping ke urutan
    def get_posisi_data(row):
        cols = [c for c in df.columns if 'Func.Loc' in c]
        for col in cols:
            if pd.notna(row[col]): return row[col]
        return "Unknown"

    df['Posisi'] = df.apply(get_posisi_data, axis=1)
    df['Urutan'] = df['Posisi'].map(order_map).fillna(5)
    df = df.sort_values('Urutan') # Sort berdasarkan alur

    # Metric Cards (Urut sesuai alur)
    cols = st.columns(4)
    labels = ['TNVDC-KARAWANG', 'TNVDC-CIBITUNG', 'TPDC-CBN', 'TCUST']
    for i, loc in enumerate(labels):
        count = len(df[df.Posisi == loc])
        cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{count}</h2></div>', unsafe_allow_html=True)

    # Tabel dengan Visualisasi Alur
    st.markdown("### 📋 Detail Status Unit")
    display_df = df.copy()
    
    # Menambahkan panah indikator pergerakan
    def get_movement(urutan):
        if urutan == 1: return "●─── 🚛 ─── ◌ ─── 🏁 ─── 👤"
        elif urutan == 2: return "○─── 🚛 ─── ● ─── 🏁 ─── 👤"
        elif urutan == 3: return "○─── 🚛 ─── ◌ ─── ● ─── 👤"
        return "○─── 🚛 ─── ◌ ─── 🏁 ─── ●"

    display_df['Pergerakan'] = display_df['Urutan'].apply(get_movement)
    
    st.write(display_df[['Posisi', 'Pergerakan', 'Customer Name_nan', 'Equipment_nan', 'Detail_nan']]
             .rename(columns={'Customer Name_nan': 'Customer', 'Equipment_nan': 'Rangka'})
             .to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("👈 Silakan upload file Excel.")
