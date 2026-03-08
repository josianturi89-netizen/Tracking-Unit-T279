import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# CSS Dark Theme dengan Branding yang Diperbesar
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Branding Box Dibuat Lebih Besar & Menonjol */
    .brand-box {
        background-color: #e60012; 
        color: white; 
        padding: 25px; 
        border-radius: 12px; 
        text-align: center; 
        font-weight: 900; 
        font-size: 1.5em; 
        line-height: 1.3;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(230, 0, 18, 0.3);
    }
    
    .metric-card { background-color: #1c2128; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }
    thead tr th { background-color: #e60012 !important; color: white !important; }
    .customer-cell { line-height: 1.2; }
    .customer-name { font-weight: bold; color: #58a6ff; font-size: 1.05em; }
    .sales-name { font-size: 0.85em; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Branding
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Hapus baris kosong
    df = df.dropna(subset=['Customer Name', 'Salesman Name'])
    
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].unique().tolist())
    sales_search = st.selectbox("👔 Filter Salesman", options=sales_list)
    f_df = df[df['Salesman Name'] == sales_search] if sales_search != "Semua Salesman" else df

    # Summary
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card" style="border-color:#58a6ff;">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    st.markdown("### 📋 Detail Status Unit")
    
    display_df = f_df.copy()
    col_show = 'Detail' if 'Detail' in display_df.columns else 'Keterangan'
    
    display_df['Customer & Salesman'] = display_df.apply(
        lambda x: f'<div class="customer-cell"><div class="customer-name">{x["Customer Name"]}</div><div class="sales-name">👤 {x["Salesman Name"]}</div></div>', 
        axis=1
    )
    
    st.write(
        display_df[['Posisi', 'Customer & Salesman', 'Equipment', col_show]].rename(
            columns={'Equipment': 'No. Rangka', col_show: 'Detail'}
        ).to_html(escape=False, index=False), 
        unsafe_allow_html=True
    )
else:
    st.info("👈 Silakan upload file Excel melalui menu di samping.")
