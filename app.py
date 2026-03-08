import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dramaga - Tracking Unit", layout="wide")

# Custom CSS untuk UI yang lebih bersih
st.markdown("""
    <style>
    .status-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .car-icon { font-size: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Branding
st.sidebar.markdown("""
    <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; text-align: center; border: 1px solid #333;">
        <h1 style="color: #FF0000; margin-bottom: 0; font-weight: bold;">Auto2000</h1>
        <h3 style="color: #FFFFFF; margin-top: 0;">Dramaga Bogor</h3>
        <hr style="border-color: #444;">
    </div>
    <br>
    """, unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("📂 Upload Database AR", type=["xlsx", "xls", "csv"])

# 3. Konten Utama
st.title("🚗 Unit Delivery Control Tower")
st.markdown("---")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # --- DATA PROCESSING ---
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
        sales_search = st.selectbox("👔 Pilih Nama Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
        cust_search = st.text_input("👤 Cari Nama Customer")

        mask = df['Customer Name'].str.contains(cust_search, case=False, na=False)
        if sales_search != "Semua Salesman":
            mask = mask & (df['Salesman Name'] == sales_search)
        
        f_df = df[mask]

        # --- UI INTERAKTIF: LOGISTIC PIPELINE ---
        st.subheader("📍 Jalur Distribusi Unit")
        
        c1, c2, c3 = st.columns(3)
        
        # Hitung Jumlah
        n_krw = f_df[f_df['Posisi Unit'] == "PABRIK (KARAWANG)"].shape[0]
        n_cbt = f_df[f_df['Posisi Unit'] == "TRANSIT (CIBITUNG)"].shape[0]
        n_cbn = f_df[f_df['Posisi Unit'] == "READY (CBN)"].shape[0]

        with c1:
            st.markdown(f'<div class="status-box" style="background-color: #ef4444;"><div class="car-icon">🏭</div><br>KARAWANG<br><h2>{n_krw} Unit</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="status-box" style="background-color: #f59e0b;"><div class="car-icon">🚛</div><br>CIBITUNG<br><h2>{n_cbt} Unit</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="status-box" style="background-color: #10b981;"><div class="car-icon">🏁</div><br>READY CBN<br><h2>{n_cbn} Unit</h2></div>', unsafe_allow_html=True)

        st.markdown("---")

        # --- TABEL DETAIL ---
        st.subheader("📋 Detail Status Unit")
        
        # Mapping Progress dengan Icon untuk Tabel
        def get_icon(status):
            if status == "READY (CBN)": return "✅ READY"
            if status == "TRANSIT (CIBITUNG)": return "🚚 ON WAY"
            if status == "PABRIK (KARAWANG)": return "🏭 FACTORY"
            return "⏳ WAIT"

        f_df['Status'] = f_df['Posisi Unit'].apply(get_icon)

        show_df = f_df[['Status', 'Customer Name', 'Salesman Name', 'Leasing Name', 'Equipment', 'Billing No', 'Billing Date', 'Keterangan']]
        st.dataframe(show_df.rename(columns={'Equipment': 'No. Rangka'}), use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error pada file: {e}")
else:
    st.info("Silakan upload file di sidebar untuk melihat pergerakan unit.")
