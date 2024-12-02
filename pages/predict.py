import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.title("Prediksi Transaksi Kartu Kredit Palsu")

# Muat model yang sudah dilatih
model_file = 'model/fraud_detection_model.pkl'
scaler_file = 'model/scaler.pkl'  # Jika menggunakan scaler (misalnya StandardScaler)

# Memuat model dan scaler (jika ada)
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Cek apakah ada scaler
try:
    with open(scaler_file, 'rb') as file:
        scaler = pickle.load(file)
except FileNotFoundError:
    scaler = None  # Jika tidak ada scaler

# Input data prediksi
account_id = st.text_input("Masukkan ID Akun atau Nomor Kartu Kredit")
amount = st.number_input("Jumlah Transaksi (Amount)")
v1 = st.number_input("Fitur V1", min_value=-100.0, max_value=100.0)
v2 = st.number_input("Fitur V2", min_value=-100.0, max_value=100.0)

# Simulasi dataset transaksi
# Misalkan ini adalah data yang tersedia dalam aplikasi atau diunggah pengguna
# Data ini hanya contoh, Anda perlu menyesuaikan dengan dataset asli
# Dalam kasus nyata, dataset ini bisa diambil dari database atau diunggah bersama file
dummy_data = {
    'account_id': ['12345', '12345', '12345', '67890', '67890', '67890', '67890'],
    'amount': [100, 200, 150, 50, 75, 80, 60],
    'v1': [0.1, -0.2, 0.3, 0.4, -0.1, 0.2, -0.3],
    'v2': [0.05, 0.02, -0.05, 0.03, -0.02, 0.01, -0.03]
}

# Mengubah data dummy ke DataFrame
df = pd.DataFrame(dummy_data)

# Proses prediksi
if st.button("Prediksi"):
    try:
        # Mengecek jumlah transaksi untuk akun yang dimasukkan
        if account_id:
            account_transactions = df[df['account_id'] == account_id]
            transaction_count = account_transactions.shape[0]
            
            # Jika jumlah transaksi < 20, akun dianggap palsu
            if transaction_count < 20:
                st.write("Akun ini dianggap **palsu** karena memiliki kurang dari 20 transaksi.")
            else:
                # Jika transaksi cukup, lakukan prediksi dengan model
                input_data = np.array([[amount, v1, v2]])  # Sesuaikan jika ada lebih banyak fitur

                # Jika model menggunakan scaler (misalnya StandardScaler), normalisasi input data
                if scaler:
                    input_data = scaler.transform(input_data)  # Skala data jika ada scaler

                # Prediksi
                prediction = model.predict(input_data)

                # Tampilkan hasil
                result = "Transaksi Palsu" if prediction[0] == 1 else "Transaksi Valid"
                st.write(f"Hasil Prediksi: {result}")

        else:
            st.warning("Mohon masukkan ID akun atau nomor kartu kredit.")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
