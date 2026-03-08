import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dark Tracker", layout="wide")

# CSS Dark Theme Profesional
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Modern Cards */
    .metric-card { 
        background-color: #1c2128; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: scale(1.02); border-color: #58a6ff; }
    
    /* Typography */
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Inter', sans-serif; }
    .stSelectbox, .stFileUploader { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🚗 Auto2000")
st.sidebar.markdown("### Dramaga Bogor")
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Logic Pemetaan
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    # Filter
    sales = st.selectbox("Pilih Nama Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
    f_df = df[df['Salesman Name'] == sales] if sales != "Semua Salesman" else df

    # 
    
    # Visual Interaktif
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card" style="border-color:#58a6ff;">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # Tabel Data
    col_show = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
    st.markdown("### 📋 Detail Status")
    st.dataframe(
        f_df[['Posisi', 'Customer Name', 'Salesman Name', 'Equipment', col_show]]
        .rename(columns={'Equipment': 'No. Rangka', col_show: 'Detail'}),
        use_container_width=True, hide_index=True
    )
else:
    st.info("Silakan upload file untuk melihat dashboard.")
