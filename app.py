import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga - Tracking", layout="wide")

# CSS: Merah Auto2000 untuk Branding, Putih bersih untuk Konten
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #000000; }
    /* Box Branding Merah */
    .branding-box { 
        background-color: #e60012; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        color: white; 
    }
    /* Metric Card Style */
    .metric-card { 
        background-color: #f4f4f4; 
        padding: 20px; 
        border-radius: 8px; 
        text-align: center; 
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="branding-box"><h1>Auto2000</h1><h3>Dramaga Bogor</h3></div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload File Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("🚛 Unit Delivery Control Tower")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Pre-processing
    df['Leasing Name'] = df['Leasing Name'].fillna('Tunai')
    
    def map_location(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_location)
    
    # Filter Salesman
    sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist())
    sales_search = st.selectbox("👔 Pilih Nama Salesman", options=sales_list)
    f_df = df[df['Salesman Name'] == sales_search] if sales_search != "Semua Salesman" else df

    # Visual Summary
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # Tabel dengan kolom 'Detail'
    col_name = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
    st.subheader("📋 Detail Unit")
    st.dataframe(
        f_df[['Posisi', 'Customer Name', 'Salesman Name', 'Equipment', col_name]]
        .rename(columns={'Equipment': 'No. Rangka', col_name: 'Detail'}), 
        use_container_width=True, hide_index=True
    )
else:
    st.info("👈 Silakan upload file Excel di menu samping.")
