import streamlit as st
import pandas as pd

st.title("Visualisasi Data")

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV untuk menampilkan data credit card secara keseluruhan", type="csv")

if uploaded_file:
    # Membaca data
    data = pd.read_csv(uploaded_file)

    # Menampilkan data yang diunggah dalam bentuk tabel
    st.write("Data yang diunggah:")
    st.dataframe(data)
