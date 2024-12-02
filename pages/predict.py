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

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV untuk analisis", type="csv")
if uploaded_file:
    try:
        # Membaca data CSV
        data = pd.read_csv(uploaded_file)

        # Memeriksa apakah kolom 'time' dan kolom dengan nama yang dimulai dengan 'V' ada
        if 'time' not in data.columns:
            st.error("File CSV tidak mengandung kolom 'time'. Pastikan kolom waktu ada dalam data.")
        else:
            v_columns = [col for col in data.columns if col.startswith('V')]  # Kolom yang dimulai dengan 'V'
            if not v_columns:
                st.error("File CSV tidak mengandung kolom yang dimulai dengan 'V'.")
            else:
                # Menampilkan kolom 'time' dan fitur 'V1-Vn'
                st.write(f"Menampilkan data untuk kolom 'time' dan fitur V1-Vn:")
                st.dataframe(data[['time'] + v_columns])

                # Deteksi anomali: jika terlalu banyak nilai negatif dalam fitur V
                # Tentukan ambang batas, misalnya 70% nilai negatif
                anomaly_threshold = 0.7
                anomalies = []
                
                # Melakukan iterasi pada setiap baris untuk deteksi anomali
                for _, row in data.iterrows():
                    # Menghitung proporsi nilai negatif pada kolom V
                    negative_values = sum(row[v_columns] < 0)  # Hitung nilai negatif pada kolom V
                    negative_percentage = negative_values / len(v_columns)
                    
                    if negative_percentage > anomaly_threshold:
                        anomalies.append(True)
                    else:
                        anomalies.append(False)
                
                # Menandai data anomali
                data['Anomaly'] = anomalies
                
                # Tampilkan data dengan deteksi anomali
                st.write("Data dengan deteksi anomali:")
                st.dataframe(data[['time'] + v_columns + ['Anomaly']])

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam memproses file: {e}")

# Input data prediksi untuk transaksi
account_id = st.text_input("Masukkan ID Akun atau Nomor Kartu Kredit")
amount = st.number_input("Jumlah Transaksi (Amount)", min_value=0.0)
v1 = st.number_input("Fitur V1", min_value=-100.0, max_value=100.0)
v2 = st.number_input("Fitur V2", min_value=-100.0, max_value=100.0)

# Simulasi dataset transaksi
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
