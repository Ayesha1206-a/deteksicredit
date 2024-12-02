import streamlit as st
import pandas as pd
import altair as alt

st.title("Visualisasi Data Transaksi")

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV untuk visualisasi", type="csv")

if uploaded_file:
    # Membaca data
    data = pd.read_csv(uploaded_file)
    st.write("Data yang diunggah:")
    st.dataframe(data.head())
    
    # Menampilkan nama kolom agar pengguna tahu kolom apa saja yang tersedia
    st.write("Kolom yang tersedia dalam dataset:", data.columns.tolist())
    
    # Memilih kolom yang berisi versi transaksi (misalnya 'version')
    version_column = st.selectbox("Pilih kolom yang menyimpan informasi versi transaksi:", data.columns.tolist())
    
    # Memastikan kolom yang dipilih ada dalam dataset
    if version_column in data.columns:
        # Menghitung jumlah transaksi berdasarkan versi
        transaction_counts = data[version_column].value_counts().reset_index()
        transaction_counts.columns = ['Version', 'Transaction Count']
        
        # Menampilkan hasil jumlah transaksi dalam bentuk tabel
        st.write("Jumlah Transaksi per Versi:")
        st.dataframe(transaction_counts)
        
        # Menampilkan grafik jumlah transaksi per versi
        chart = alt.Chart(transaction_counts).mark_bar().encode(
            x='Version:N',
            y='Transaction Count:Q',
            color='Version:N',
            tooltip=['Version', 'Transaction Count']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning(f"Kolom '{version_column}' tidak ditemukan dalam data.")
