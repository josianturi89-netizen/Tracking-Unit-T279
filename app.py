import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# CSS Dark Theme & Branding
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Branding Box Merah */
    .brand-box {
        background-color: #e60012;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .metric-card { 
        background-color: #1c2128; border: 1px solid #30363d; 
        border-radius: 12px; padding: 20px; text-align: center;
    }
    
    .user-info { font-size: 0.85em; color: #8b949e; }
    .customer-name { font-size: 1em; font-weight: bold; color: #58a6ff; }
    
    /* Tabel Header Style */
    thead tr th {
        background-color: #e60012 !important;
        color: white !important;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Branding Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    # Membaca data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Mapping Posisi
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    # Filter
    sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist())
    sales_search = st.selectbox("👔 Filter Salesman", options=sales_list)
    f_df = df[df['Salesman Name'] == sales_search] if sales_search != "Semua Salesman" else df

    # Summary Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card" style="border-color:#58a6ff;">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # Menangani kolom Detail
    col_show = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
    
    # Menyiapkan tabel untuk ditampilkan
    display_df = f_df.copy()
    display_df['Sales & Customer'] = display_df.apply(
        lambda x: f'{x["Customer Name"]} | Sales: {x["Salesman Name"]}', axis=1
    )
    
    st.markdown("### 📋 Detail Status")
    
    # Menampilkan data
    st.dataframe(
        display_df[['Posisi', 'Sales & Customer', 'Equipment', col_show]].rename(
            columns={'Equipment': 'No. Rangka', col_show: 'Detail', 'Sales & Customer': 'Customer & Salesman'}
        ), 
        use_container_width=True, hide_index=True
    )
else:
    st.info("Silakan upload file untuk memulai.")
