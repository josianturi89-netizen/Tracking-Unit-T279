import streamlit as st
import pandas as pd

# Konfigurasi Halaman Minimalis
st.set_page_config(page_title="Auto2000 Delivery Tracker", layout="wide")

# CSS Modern Minimalist
st.markdown("""
    <style>
    /* Global Styles */
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #1a1a1a; font-family: sans-serif; }
    
    /* Process Stepper Styles */
    .stepper { display: flex; justify-content: space-between; margin: 20px 0; }
    .step { 
        flex: 1; padding: 15px; text-align: center; 
        border-bottom: 3px solid #e0e0e0; color: #777; 
    }
    .step.active { border-bottom: 3px solid #007bff; color: #007bff; font-weight: bold; }
    
    /* Card Style */
    .metric-card { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## **Auto2000**")
st.sidebar.markdown("Dramaga Bogor | Monitoring Dashboard")
uploaded_file = st.sidebar.file_uploader("Upload Data AR (Excel/CSV)", type=["xlsx", "csv"])

# Main Content
st.title("Unit Delivery Journey")
st.markdown("Pantau posisi unit dari pabrik hingga siap kirim.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Mapping Location (Process Stages)
    def get_status_code(loc):
        loc = str(loc).upper()
        if "CBN" in loc: return 3
        elif "CIBITUNG" in loc: return 2
        elif "KARAWANG" in loc: return 1
        return 0

    df['Stage'] = df['Func.Loc'].apply(get_status_code)
    
    # Filter
    sales = st.selectbox("Pilih Salesman", ["Semua Salesman"] + sorted(df['Salesman Name'].dropna().unique().tolist()))
    f_df = df[df['Salesman Name'] == sales] if sales != "Semua Salesman" else df

    # --- MODERN STEPPER UI ---
    st.markdown("""
    <div class="stepper">
        <div class="step active">🏭 1. PABRIK</div>
        <div class="step active">🚛 2. TRANSIT</div>
        <div class="step active">🏁 3. READY (CBN)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">Total di Pabrik<br><h2>{len(f_df[f_df.Stage==1])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">Total Transit<br><h2>{len(f_df[f_df.Stage==2])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">Siap Kirim (CBN)<br><h2>{len(f_df[f_df.Stage==3])}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Clean Data Table
    display_df = f_df[['Func.Loc', 'Customer Name', 'Salesman Name', 'Equipment', 'Keterangan']]
    st.dataframe(display_df.rename(columns={'Equipment': 'No. Rangka'}), use_container_width=True, hide_index=True)

else:
    st.info("Silakan unggah data untuk memulai.")
