import streamlit as st
import pandas as pd

st.title("Visualisasi Data")

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV untuk visualisasi", type="csv")

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file:
    try:
        # Memuat data menggunakan cache
        data = load_data(uploaded_file)
        
        # Tampilkan data yang diunggah (hanya 100 baris pertama untuk mempercepat tampilan)
        st.write("Data yang diunggah (100 baris pertama):")
        st.dataframe(data.head(100))

        # Informasi tentang ukuran dataset
        st.write(f"Jumlah baris dan kolom: {data.shape[0]} baris, {data.shape[1]} kolom")

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam memproses file: {e}")
