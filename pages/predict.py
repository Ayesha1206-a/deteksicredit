import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

st.title("Prediksi Transaksi Kartu Kredit Palsu")

# Muat model yang sudah dilatih dengan pengecekan file
model_file = 'model/fraud_detection_model.pkl'
if not os.path.exists(model_file):
    st.error(f"File model tidak ditemukan di {model_file}. Pastikan file model tersedia.")
else:
    try:
        with open(model_file, 'rb') as file:
            model = pickle.load(file)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat model: {e}")

    # Pengguna mengunggah file CSV
    uploaded_file = st.file_uploader("Unggah File CSV untuk Prediksi", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Membaca file CSV
            data = pd.read_csv(uploaded_file)
            
            # Menampilkan preview data untuk memastikan file berhasil dibaca
            st.write("Data yang diunggah:")
            st.dataframe(data.head())

            # Pastikan bahwa data memiliki kolom yang sesuai dengan model
            required_columns = ['Amount', 'V1', 'V2', 'V3']  # Sesuaikan dengan kolom yang digunakan model Anda
            if not all(col in data.columns for col in required_columns):
                st.error(f"File CSV harus mengandung kolom: {', '.join(required_columns)}")
            else:
                # Menambahkan kolom untuk kategori prediksi berdasarkan V1, V2, V3...
                # Mencari nilai terendah (paling negatif) di kolom V1, V2, V3
                v_columns = ['V1', 'V2', 'V3']  # Sesuaikan dengan nama kolom V yang digunakan
                data['Min_V'] = data[v_columns].min(axis=1)  # Mencari nilai terendah pada setiap baris
                
                # Tentukan kategori berdasarkan nilai V terendah
                data['Prediksi'] = data['Min_V'].apply(lambda x: "Transaksi Palsu" if x < -1 else "Transaksi Valid")

                # Menampilkan hasil prediksi
                st.write("Hasil Prediksi:")
                st.dataframe(data)

        except pd.errors.EmptyDataError:
            st.error("File CSV yang diunggah kosong.")
        except pd.errors.ParserError:
            st.error("Terjadi kesalahan saat membaca file CSV. Pastikan file CSV valid dan formatnya benar.")
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses file: {e}")
