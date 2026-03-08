import streamlit as st
import pandas as pd

# Konfigurasi Halaman Dark Theme
st.set_page_config(page_title="Auto2000 Dark Tracker", layout="wide")

# CSS untuk Dark Theme & UI Modern
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .metric-card { 
        background-color: #1c2128; border: 1px solid #30363d; 
        border-radius: 12px; padding: 20px; text-align: center;
    }
    .user-info { font-size: 0.9em; color: #8b949e; }
    .customer-name { font-size: 1.1em; font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🚗 Auto2000")
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
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

    # Summary
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card" style="border-color:#58a6ff;">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # GABUNGAN KOLOM (SALES & CUSTOMER)
    st.markdown("### 📋 Detail Status")
    
    # Membuat kolom baru untuk tampilan
    display_df = f_df.copy()
    display_df['Sales & Customer'] = display_df.apply(
        lambda x: f'<div class="customer-name">{x["Customer Name"]}</div><div class="user-info">👤 {x["Salesman Name"]}</div>', 
        axis=1
    )
    
    # Menampilkan tabel dengan HTML (Streamlit akan merender HTML di kolom)
    col_show = 'Detail' if 'Detail' in display_df.columns else 'Keterangan'
    
    st.write(
        display_df[['Posisi', 'Sales & Customer', 'Equipment', col_show]].rename(
            columns={'Equipment': 'No. Rangka', col_show: 'Detail'}
        ).to_html(escape=False, index=False), 
        unsafe_allow_html=True
    )
else:
    st.info("Silakan upload file untuk memulai.")
