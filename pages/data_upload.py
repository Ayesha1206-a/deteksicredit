import streamlit as st
import pandas as pd

st.title("Visualisasi Data Transaksi Kartu Kredit")

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV untuk visualisasi", type="csv")

if uploaded_file:
    # Membaca data
    data = pd.read_csv(uploaded_file)

    # Menampilkan kolom yang ada di dalam dataset
    st.write("Kolom yang tersedia dalam dataset:", data.columns.tolist())

    # Memastikan kolom 'time' ada dan mengonversinya ke datetime
    if 'time' in data.columns:
        data['time'] = pd.to_datetime(data['time'], errors='coerce')  # Mengubah kolom 'time' menjadi format datetime
        st.write("Kolom 'time' berhasil diubah menjadi format waktu.")
    else:
        st.warning("Kolom 'time' tidak ditemukan dalam dataset. Pastikan kolom ini ada untuk memproses waktu transaksi.")

    # Menyaring kolom akun yang dimulai dengan 'v' (v1, v2, v3, ...)
    account_columns = [col for col in data.columns if col.startswith('v')]
    if account_columns:
        st.write(f"Akun terdeteksi pada kolom: {account_columns}")
    else:
        st.warning("Tidak ditemukan kolom akun yang dimulai dengan 'v'. Pastikan kolom akun dimulai dengan 'v' seperti 'v1', 'v2', dll.")

    # Menampilkan data yang diunggah
    st.write("Data yang diunggah:")
    st.dataframe(data)

    # Menampilkan statistik umum dataset
    st.write("Statistik Deskriptif Data:")
    st.write(data.describe())

    # Menampilkan informasi lengkap tentang tipe data kolom
    st.write("Info Data:")
    st.write(data.info())
