import streamlit as st
import pandas as pd

# (Gunakan bagian CSS Dark Theme yang sebelumnya)

# ... (setelah proses f_df di kode sebelumnya)

    # 1. Pilih kolom yang akan ditampilkan
    col_show = 'Detail' if 'Detail' in f_df.columns else 'Keterangan'
    tabel_final = f_df[['Posisi', 'Customer Name', 'Salesman Name', 'Equipment', col_show]].rename(
        columns={'Equipment': 'No. Rangka', col_show: 'Detail', 'Posisi': 'Status Unit'}
    )

    # 2. Menggunakan Pandas Styler untuk menghighlight Header
    def highlight_header(s):
        return 'background-color: #e60012; color: #ffffff; font-weight: bold; text-align: center;'

    # Terapkan styling
    styled_table = tabel_final.style.set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#e60012'), ('color', 'white'), ('text-align', 'center'), ('border', '1px solid #333')]
    }])

    st.markdown("### 📋 Detail Status Unit")
    st.dataframe(styled_table, use_container_width=True, hide_index=True)
