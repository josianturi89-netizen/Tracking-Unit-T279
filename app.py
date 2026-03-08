import streamlit as st
import pandas as pd

# Konfigurasi Halaman Minimalis
st.set_page_config(page_title="Auto2000 Tracker", layout="wide")

# CSS untuk UI Modern & Minimalis
st.markdown("""
    <style>
    /* Background Putih Bersih */
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* Font Hitam Profesional */
    h1, h2, h3, p, div { color: #1a1a1a !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Kartu Status Modern */
    .status-card { 
        background-color: #f8f9fa; 
        border: 1px solid #e0e0e0;
        padding: 20px; 
        border-radius: 12px; 
        text-align: center; 
        transition: 0.3s;
    }
    .status-card:hover { border-color: #007bff; }
    
    /* Tombol Aksen Biru */
    .stButton>button { border-radius: 8px; border: none; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Sederhana
st.sidebar.title("Auto2000")
st.sidebar.subheader("Dramaga Bogor")
uploaded_file = st.sidebar.file_uploader("Upload Excel Data AR", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Tracker")
st.markdown("Pantau posisi unit real-time dengan tampilan bersih.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Mapping Data
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    # Filter Salesman
    sales = st.selectbox("Pilih Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
    f_df = df[df['Salesman Name'] == sales] if sales != "Semua Salesman" else df

    # 
    
    # Visual Cards Modern
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="status-card">🏭 Pabrik<br><strong>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</strong></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="status-card">🚛 Transit<br><strong>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</strong></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="status-card" style="border-left: 5px solid #007bff;">🏁 Ready CBN<br><strong>{len(f_df[f_df.Posisi=="READY (CBN)"])}</strong></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabel Minimalis
    st.dataframe(
        f_df[['Posisi', 'Customer Name', 'Salesman Name', 'Equipment', 'Keterangan']]
        .rename(columns={'Equipment': 'No. Rangka'}),
        use_container_width=True, hide_index=True
    )
else:
    st.info("Silakan unggah file data untuk menampilkan dashboard.")
