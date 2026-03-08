import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga - Tracking", layout="wide")

# CSS untuk UI Mobile Friendly
st.markdown("""
    <style>
    .status-box { padding: 15px; border-radius: 12px; text-align: center; color: white; font-weight: bold; margin: 5px; }
    .car-icon { font-size: 25px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Branding
st.sidebar.markdown("""
    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: #FF0000; margin:0;">Auto2000</h1>
        <h3 style="color: #FFFFFF; margin:0;">Dramaga Bogor</h3>
    </div><br>
    """, unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("📂 Upload File Excel/CSV", type=["xlsx", "xls", "csv"])

# Konten Utama
st.title("🚛 Unit Delivery Control Tower")

if uploaded_file is not None:
    # Load Data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Pre-processing
    df['Leasing Name'] = df['Leasing Name'].fillna('Tunai')
    if 'Post Date' in df.columns:
        df['Billing Date'] = pd.to_datetime(df['Post Date'], errors='coerce').dt.strftime('%d-%m-%Y')

    def map_location(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi Unit'] = df['Func.Loc'].apply(map_location)

    # Filter
    sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist())
    sales_search = st.selectbox("👔 Pilih Nama Salesman", options=sales_list)
    f_df = df[df['Salesman Name'] == sales_search] if sales_search != "Semua Salesman" else df

    # UI Visual Pipeline
    c1, c2, c3 = st.columns(3)
    n_krw = f_df[f_df['Posisi Unit'] == "PABRIK (KARAWANG)"].shape[0]
    n_cbt = f_df[f_df['Posisi Unit'] == "TRANSIT (CIBITUNG)"].shape[0]
    n_cbn = f_df[f_df['Posisi Unit'] == "READY (CBN)"].shape[0]

    c1.markdown(f'<div class="status-box" style="background-color: #ef4444;"><div class="car-icon">🏭</div>KARAWANG<br><h2>{n_krw}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="status-box" style="background-color: #f59e0b;"><div class="car-icon">🚛</div>CIBITUNG<br><h2>{n_cbt}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="status-box" style="background-color: #10b981;"><div class="car-icon">🏁</div>READY CBN<br><h2>{n_cbn}</h2></div>', unsafe_allow_html=True)

    # Tabel
    st.dataframe(
        f_df[['Posisi Unit', 'Customer Name', 'Salesman Name', 'Leasing Name', 'Equipment', 'Billing Date', 'Keterangan']]
        .rename(columns={'Equipment': 'No. Rangka'}), 
        use_container_width=True, hide_index=True
    )
else:
    st.info("👈 Silakan upload file Excel/CSV di menu samping untuk memulai dashboard.")
    

[Image of logistics supply chain process]
