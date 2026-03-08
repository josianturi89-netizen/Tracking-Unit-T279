import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# (CSS Anda tetap sama, saya tambahkan sedikit style untuk chart)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .brand-box { background-color: #e60012; color: white; padding: 25px; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1.5em; margin-bottom: 25px; }
    .metric-card { background-color: #1c2128; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }
    thead tr th { background-color: #e60012 !important; color: white !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    df = df.dropna(subset=['Customer Name', 'Salesman Name'])
    
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    # Filter
    sales = st.selectbox("👔 Filter Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].unique().tolist()))
    f_df = df[df['Salesman Name'] == sales] if sales != "Semua Salesman" else df

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # --- TAMBAHAN: MATRIX CHART ---
    st.markdown("### 📊 Distribusi Posisi Unit")
    col_chart, col_table = st.columns([1, 2])
    
    with col_chart:
        # Menghitung data untuk chart
        chart_data = f_df['Posisi'].value_counts().reset_index()
        chart_data.columns = ['Posisi', 'Jumlah']
        st.bar_chart(chart_data.set_index('Posisi'))
        st.caption("Visualisasi perbandingan volume unit per lokasi.")

    with col_table:
        st.markdown("### 📋 Detail Status Unit")
        col_show = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
        display_df = f_df.copy()
        display_df['Customer & Salesman'] = display_df.apply(lambda x: f'<b>{x["Customer Name"]}</b><br><small>👤 {x["Salesman Name"]}</small>', axis=1)
        st.write(display_df[['Posisi', 'Customer & Salesman', 'Equipment', col_show]].rename(columns={'Equipment': 'No. Rangka', col_show: 'Detail'}).to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("👈 Silakan upload file Excel untuk memulai.")

# Sembunyikan menu
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)
