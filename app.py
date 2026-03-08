import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# CSS dan Theme Setup
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
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

if uploaded_file is not None:
    # 1. Membaca header 2 baris
    df = pd.read_excel(uploaded_file, header=[0, 1])
    
    # 2. Menggabungkan header menjadi satu nama kolom agar tidak error
    df.columns = ['_'.join(map(str, col)).replace('_nan', '').strip() for col in df.columns.values]
    
    # 3. Identifikasi kolom secara fleksibel
    col_map = {
        'Customer': [c for c in df.columns if 'Customer Name' in c][0],
        'Salesman': [c for c in df.columns if 'Salesman Name' in c][0],
        'Equip': [c for c in df.columns if 'Equipment' in c][0],
        'Detail': [c for c in df.columns if 'Detail' in c][0]
    }
    func_cols = [c for c in df.columns if 'Func.Loc' in c]
    
    # 4. Ambil posisi dan urutkan
    def get_posisi(row):
        for col in func_cols:
            if pd.notna(row[col]): return row[col]
        return "Unknown"

    df['Posisi'] = df.apply(get_posisi, axis=1)
    
    # Urutan sesuai permintaan
    order_map = {'TNVDC-KARAWANG': 1, 'TNVDC-CIBITUNG': 2, 'TPDC-CBN': 3, 'TCUST': 4}
    df['Urutan'] = df['Posisi'].map(order_map).fillna(5)
    
    # 5. Tampilan Dashboard
    st.title("Unit Delivery Control Tower")
    cols = st.columns(4)
    labels = ['TNVDC-KARAWANG', 'TNVDC-CIBITUNG', 'TPDC-CBN', 'TCUST']
    for i, loc in enumerate(labels):
        count = len(df[df.Posisi == loc])
        cols[i].markdown(f'<div class="metric-card">📍 {loc}<br><h2>{count}</h2></div>', unsafe_allow_html=True)

    st.markdown("### 📋 Detail Status Unit")
    display_df = df.sort_values('Urutan').copy()
    
    # Visualisasi panah pergerakan
    def get_move(u): return "●── 🚛 ── ◌ ── 🏁 ── 👤" if u==1 else "○── 🚛 ── ● ── 🏁 ── 👤" if u==2 else "○── 🚛 ── ◌ ── ● ── 👤" if u==3 else "○── 🚛 ── ◌ ── 🏁 ── ●"
    display_df['Pergerakan'] = display_df['Urutan'].apply(get_move)
    
    st.write(display_df[[col_map['Customer'], col_map['Salesman'], col_map['Equip'], 'Posisi', 'Pergerakan']].to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("👈 Silakan upload file Excel.")
