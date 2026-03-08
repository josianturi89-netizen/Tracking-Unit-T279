import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# Inisialisasi state untuk tema
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

# Fungsi untuk memilih tema
theme_mode = st.sidebar.radio("🎨 Pilih Mode Tampilan:", ['Dark', 'White'], index=0 if st.session_state.theme == 'Dark' else 1)
st.session_state.theme = theme_mode

# Konfigurasi CSS Dinamis
if st.session_state.theme == 'Dark':
    bg_color, text_color, card_bg, border_color = "#0e1117", "#ffffff", "#1c2128", "#30363d"
else:
    bg_color, text_color, card_bg, border_color = "#ffffff", "#000000", "#f0f2f6", "#d1d5db"

header_color = "#e60012"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .brand-box {{ background-color: {header_color}; color: white; padding: 25px; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1.5em; margin-bottom: 25px; }}
    .metric-card {{ background-color: {card_bg}; border: 1px solid {border_color}; border-radius: 12px; padding: 20px; text-align: center; }}
    thead tr th {{ background-color: {header_color} !important; color: white !important; text-align: center !important; }}
    .customer-name {{ font-weight: bold; color: {'#e60012' if st.session_state.theme == 'White' else '#58a6ff'}; }}
    .sales-name {{ font-size: 0.85em; color: #8b949e; }}
    </style>
    """, unsafe_allow_html=True)

# Branding
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

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
    
    sales_list = ["Semua Salesman"] + sorted(df['Salesman Name'].unique().tolist())
    sales_search = st.selectbox("👔 Filter Salesman", options=sales_list)
    f_df = df[df['Salesman Name'] == sales_search] if sales_search != "Semua Salesman" else df

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="metric-card">🏭 Pabrik<br><h2>{len(f_df[f_df.Posisi=="PABRIK (KARAWANG)"])}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">🚛 Transit<br><h2>{len(f_df[f_df.Posisi=="TRANSIT (CIBITUNG)"])}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">🏁 Ready CBN<br><h2>{len(f_df[f_df.Posisi=="READY (CBN)"])}</h2></div>', unsafe_allow_html=True)

    # LAYOUT BARU: Chart (Kiri) & Tabel (Kanan)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 Distribusi Unit")
        chart_data = f_df['Posisi'].value_counts().reset_index()
        chart_data.columns = ['Posisi', 'Total']
        fig = px.bar(chart_data, x='Posisi', y='Total', color='Posisi', 
                     color_discrete_sequence=['#e60012', '#58a6ff', '#ffaa33'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False, font_color=text_color)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📋 Detail Status Unit")
        col_show = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
        display_df = f_df.copy()
        display_df['Customer & Salesman'] = display_df.apply(
            lambda x: f'<div class="customer-cell"><div class="customer-name">{x["Customer Name"]}</div><div class="sales-name">👤 {x["Salesman Name"]}</div></div>', axis=1
        )
        st.write(display_df[['Posisi', 'Customer & Salesman', 'Equipment', col_show]].rename(columns={'Equipment': 'No. Rangka', col_show: 'Detail'}).to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    st.info("👈 Silakan upload file Excel untuk memulai.")

st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)
