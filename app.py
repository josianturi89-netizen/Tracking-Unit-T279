import streamlit as st
import pandas as pd

# Konfigurasi Halaman Modern
st.set_page_config(page_title="Auto2000 Tracking", layout="wide")

# CSS untuk UI Modern Putih & Soft Biru
st.markdown("""
    <style>
    .main { background-color: #f8fbff; }
    .stApp { background-color: #f8fbff; }
    .stepper-box { 
        background: white; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #007bff; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .metric-card { background: #eef6ff; padding: 15px; border-radius: 10px; text-align: center; }
    h1, h2, h3 { color: #003366; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Branding
st.sidebar.markdown("""
    <div style="background-color: #003366; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h1 style="color: #FF0000;">Auto2000</h1>
        <h3>Dramaga Bogor</h3>
    </div><br>
    """, unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("📂 Upload Data AR", type=["xlsx", "csv"])

# Konten Utama
st.title("📍 Unit Logistics Journey")
st.markdown("Pantau posisi unit dari pabrik hingga ke tangan pelanggan.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Mapping Lokasi Modern
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return 3 # Finish
        elif "CIBITUNG" in loc: return 2 # Transit
        elif "KARAWANG" in loc: return 1 # Factory
        return 0

    df['Status_Level'] = df['Func.Loc'].apply(map_status)
    
    # Filter
    sales = st.selectbox("👔 Pilih Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
    f_df = df[df['Salesman Name'] == sales] if sales != "Semua Salesman" else df

    # Visual Stepper UI
    st.subheader("📊 Monitoring Alur Unit")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Status_Level==1])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Status_Level==2])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">🏁 Ready CBN<br><h2>{len(f_df[f_df.Status_Level==3])}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Daftar Unit")
    
    # Tabel dengan Highlight Status
    display_df = f_df.copy()
    display_df['Progress'] = display_df['Status_Level'].map({1: '🏭 FACTORY', 2: '🚛 TRANSIT', 3: '🏁 READY CBN', 0: '⏳ PROSES'})
    
    st.dataframe(
        display_df[['Progress', 'Customer Name', 'Salesman Name', 'Equipment', 'Keterangan']],
        use_container_width=True, hide_index=True
    )
else:
    st.info("Silakan upload file Excel untuk melihat alur distribusi unit.")
