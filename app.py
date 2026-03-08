import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi
st.set_page_config(page_title="Auto2000 Dashboard", layout="wide")

# CSS untuk desain modern & sidebar
st.markdown("""
    <style>
    .brand-box { background-color: #e60012; color: white; padding: 25px; border-radius: 12px; text-align: center; font-weight: 900; font-size: 1.5em; margin-bottom: 25px; }
    .metric-card { background-color: #1c2128; border: 1px solid #30363d; border-radius: 12px; padding: 20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="brand-box">AUTO2000<br>Dramaga Bogor</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("📂 Upload Data Excel", type=["xlsx", "csv"])

st.title("Unit Delivery Control Tower")

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    df = df.dropna(subset=['Customer Name', 'Salesman Name'])
    
    # Mapping
    df['Posisi'] = df['Func.Loc'].apply(lambda x: "READY (CBN)" if "CBN" in str(x).upper() else ("TRANSIT (CIBITUNG)" if "CIBITUNG" in str(x).upper() else "PABRIK (KARAWANG)"))
    
    # --- MODERN MATRIX CHART ---
    # Menghitung data
    chart_data = df.groupby('Posisi').size().reset_index(name='Jumlah')
    
    # Membuat Chart menggunakan Plotly untuk tampilan premium
    fig = px.bar(chart_data, x='Posisi', y='Jumlah', color='Posisi',
                 color_discrete_map={'READY (CBN)': '#58a6ff', 'TRANSIT (CIBITUNG)': '#ffaa33', 'PABRIK (KARAWANG)': '#e60012'},
                 text='Jumlah')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    
    # Layout Utama
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.subheader("📊 Distribusi Posisi")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_r:
        st.subheader("📋 Detail Status Unit")
        # Menampilkan data
        display_df = df[['Posisi', 'Customer Name', 'Salesman Name', 'Equipment']]
        st.dataframe(display_df, use_container_width=True)
else:
    st.info("Silakan upload data.")
