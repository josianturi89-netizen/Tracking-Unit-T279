import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# CSS Dark Theme & Modern Table Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Branding Box */
    .brand-box {
        background-color: #e60012; color: white; padding: 15px;
        border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 20px;
    }
    
    /* Metric Card Modern */
    .metric-card { 
        background-color: #1c2128; border: 1px solid #30363d; 
        border-radius: 12px; padding: 20px; text-align: center;
    }
    
    /* Tabel Header Red Highlight */
    thead tr th { background-color: #e60012 !important; color: white !important; }
    
    /* Stacked Text Styling */
    .customer-cell { line-height: 1.2; }
    .customer-name { font-weight: bold; color: #58a6ff; font-size: 1.05em; }
    .sales-name { font-size: 0.85em; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

# Konten Utama
st.title("Unit Delivery Control Tower")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Logic Pemetaan Posisi
    def map_status(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return "READY (CBN)"
        elif "CIBITUNG" in loc: return "TRANSIT (CIBITUNG)"
        elif "KARAWANG" in loc: return "PABRIK (KARAWANG)"
        return "PROSES"

    df['Posisi'] = df['Func.Loc'].apply(map_status)
    
    # Filter Salesman
    sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist())
    sales_search = st.selectbox("👔 Filter Salesman", options=sales_list)
    f_df = df[df['Salesman Name'] == sales_search] if sales_search != "Semua Salesman" else df

    # 

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card" style="border-color:#58a6ff;">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # Tabel Modern Stacked
    st.markdown("### 📋 Detail Status Unit")
    
    display_df = f_df.copy()
    col_show = 'Detail' if 'Detail' in display_df.columns else 'Keterangan'
    
    # Membuat kolom gabungan dengan HTML
    display_df['Customer & Salesman'] = display_df.apply(
        lambda x: f'<div class="customer-cell"><div class="customer-name">{x["Customer Name"]}</div><div class="sales-name">👤 {x["Salesman Name"]}</div></div>', 
        axis=1
    )
    
    # Render Tabel
    st.write(
        display_df[['Posisi', 'Customer & Salesman', 'Equipment', col_show]].rename(
            columns={'Equipment': 'No. Rangka', col_show: 'Detail'}
        ).to_html(escape=False, index=False), 
        unsafe_allow_html=True
    )
else:
    st.info("👈 Silakan upload file Excel melalui menu di samping.")
