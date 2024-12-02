import streamlit as st
import pandas as pd

st.title("Unggah Data Transaksi Kartu Kredit")

uploaded_file = st.file_uploader("Unggah file CSV", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Data yang diunggah:")
    st.dataframe(data.head())
