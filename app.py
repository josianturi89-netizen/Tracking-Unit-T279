import streamlit as st
import pandas as pd

# Konfigurasi Halaman - Menjaga tata letak agar rapi di Mobile & Laptop
st.set_page_config(page_title="Auto2000 Delivery Tracker", layout="wide")

# CSS untuk desain High-Contrast agar mudah dibaca mata
st.markdown("""
    <style>
    /* Background Putih & Font Hitam */
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* Judul & Teks Utama */
    h1, h2, h3, div { color: #000000 !important; font-family: sans-serif; }
    
    /* Kartu Metrik dengan batas tegas */
    .metric-card { 
        background-color: #f0f2f6; 
        border: 2px solid #0056b3; 
        padding: 20px; 
        border-radius: 8px; 
        text-align: center; 
        margin-bottom: 10px;
    }
    
    /* Highlight untuk Ready CBN */
    .ready-card { border: 2px solid #28a745; background-color: #e9f7ef; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Auto2000 Dramaga")
uploaded_file = st.sidebar.file_uploader("Upload Data Excel", type=["xlsx", "csv"])

# Main
st.title("Unit Delivery Journey")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Pre-processing & Smart Mapping
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "LAINNYA"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    # Filter
    sales = st.selectbox("Pilih Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
    f_df = df[df['Salesman Name'] == sales] if sales != "Semua Salesman" else df

    # Visual Summary
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><strong>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</strong></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><strong>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</strong></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card ready-card">🏁 Ready CBN<br><strong>{len(f_df[f_df.Posisi=="READY (CBN)"])}</strong></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabel menggunakan kolom 'Detail' sesuai request Anda
    # Memastikan kolom 'Detail' ada, jika tidak, kita gunakan keterangan sebagai backup
    col_to_show = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
    
    st.subheader("📋 Detail Unit")
    st.dataframe(
        f_df[['Posisi', 'Customer Name', 'Salesman Name', 'Equipment', col_to_show]]
        .rename(columns={'Equipment': 'No. Rangka', col_to_show: 'Detail'}),
        use_container_width=True, hide_index=True
    )
else:
    st.info("Silakan unggah file data untuk memulai.")
