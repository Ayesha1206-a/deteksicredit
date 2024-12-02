import streamlit as st
import pickle
import numpy as np

st.title("Prediksi Transaksi Kartu Kredit Palsu")

# Muat model yang sudah dilatih
model_file = 'model/fraud_detection_model.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Input data prediksi
amount = st.number_input("Jumlah Transaksi (Amount)")
v1 = st.number_input("Fitur V1", min_value=-100.0, max_value=100.0)
v2 = st.number_input("Fitur V2", min_value=-100.0, max_value=100.0)
# Tambahkan input untuk fitur lain dari dataset

# Proses prediksi
if st.button("Prediksi"):
    try:
        input_data = np.array([[amount, v1, v2]])  # Sesuaikan dengan fitur yang ada
        prediction = model.predict(input_data)
        result = "Transaksi Palsu" if prediction[0] == 1 else "Transaksi Valid"
        st.write(f"Hasil Prediksi: {result}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
