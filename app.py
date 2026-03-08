import streamlit as st
import pandas as pd
import os

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga - Realtime Monitoring", layout="wide")

# Custom CSS untuk UI Mobile Friendly
st.markdown("""
    <style>
    .status-box { padding: 15px; border-radius: 10px; text-align: center; color: white; margin-bottom: 10px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Branding
st.sidebar.markdown("""
    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="color: #FF0000; margin:0;">Auto2000</h1>
        <h3 style="color: #FFFFFF; margin:0;">Dramaga Bogor</h3>
    </div><br>
    """, unsafe_allow_html=True)

# --- LOGIKA DATABASE OTOMATIS ---
# Nama file yang harus ada di GitHub Anda
DATA_FILE = "data.xlsx"

@st.cache_data(ttl=60) # Refresh data setiap 60 detik jika ada perubahan di GitHub
def load_data(file):
    if file.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Cek apakah file data.xlsx ada di repository
if os.path.exists(DATA_FILE):
    df_raw = load_data(DATA_FILE)
    st.sidebar.success("✅ Menggunakan Database Terpusat")
else:
    st.sidebar.warning("⚠️ File data.xlsx tidak ditemukan di GitHub.")
    uploaded = st.sidebar.file_uploader("Upload Manual (Hanya Sementera)", type=["xlsx", "csv"])
    if uploaded:
        df_raw = load_data(uploaded)
    else:
        st.stop()

# --- PROCESSING DATA ---
df = df_raw.copy()
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

# --- FILTER ---
st.subheader("🔍 Monitoring Unit Salesman")
sales_search = st.selectbox("👔 Nama Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
mask = df['Salesman Name'] == sales_search if sales_search != "Semua Salesman" else df['Salesman Name'].notnull()
f_df = df[mask]

# --- UI MOBILE FRIENDLY ---
c1, c2, c3 = st.columns(3)
n_krw = f_df[f_df['Posisi Unit'] == "PABRIK (KARAWANG)"].shape[0]
n_cbt = f_df[f_df['Posisi Unit'] == "TRANSIT (CIBITUNG)"].shape[0]
n_cbn = f_df[f_df['Posisi Unit'] == "READY (CBN)"].shape[0]

c1.markdown(f'<div class="status-box" style="background-color: #ef4444;">🏭 KARAWANG<br><h2>{n_krw}</h2></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="status-box" style="background-color: #f59e0b;">🚛 CIBITUNG<br><h2>{n_cbt}</h2></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="status-box" style="background-color: #10b981;">🏁 READY CBN<br><h2>{n_cbn}</h2></div>', unsafe_allow_html=True)

st.dataframe(f_df[['Posisi Unit', 'Customer Name', 'Leasing Name', 'Equipment', 'Billing Date', 'Keterangan']].rename(columns={'Equipment': 'No. Rangka'}), use_container_width=True, hide_index=True)
