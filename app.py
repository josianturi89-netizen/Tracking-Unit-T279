import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tracking Unit", layout="wide")
st.title("🚛 Unit Logistics Tracking")

uploaded_file = st.sidebar.file_uploader("Upload File Excel/CSV", type=["csv", "xlsx"])

if uploaded_file:
    # Membaca data
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Menampilkan ringkasan cepat
    st.subheader("Monitoring Unit")
    
    # Filter per Kolom
    col1, col2 = st.columns(2)
    with col1:
        search_cust = st.text_input("Cari Customer")
    with col2:
        search_sales = st.text_input("Cari Salesman")
        
    filtered_df = df[df['Customer Name'].str.contains(search_cust, case=False, na=False)]
    filtered_df = filtered_df[filtered_df['Salesman Name'].str.contains(search_sales, case=False, na=False)]
    
    st.dataframe(filtered_df[['Customer Name', 'Salesman Name', 'Func.Loc', 'Age', 'Keterangan']], use_container_width=True)
else:
    st.info("Silakan upload file di sidebar sebelah kiri.")
