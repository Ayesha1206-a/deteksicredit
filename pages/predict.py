import pickle
import pandas as pd

# Memuat model yang telah dilatih
with open('model/fraud_detection_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Fungsi untuk memproses data
def process_data(file):
    # Memuat data CSV
    data = pd.read_csv(file)
    
    # Memastikan bahwa data yang dimuat memiliki kolom yang diinginkan
    if 'Class' in data.columns:
        features = data.drop(['Class'], axis=1)  # Menghapus kolom target 'Class'
    else:
        features = data  # Jika tidak ada kolom target, ambil semua fitur
    
    return features, data

# Fungsi untuk memprediksi dan menampilkan hasil
def predict(file):
    # Proses data
    features, data = process_data(file)
    
    # Prediksi menggunakan model
    predictions = model.predict(features)
    
    # Menambahkan kolom 'Prediction' untuk menunjukkan apakah transaksi fraud
    data['Prediction'] = predictions
    data['Prediction'] = data['Prediction'].map({0: 'Valid', 1: 'Fraud'})
    
    return data

# Menyediakan path file CSV
file_path = input("Masukkan path file CSV yang berisi transaksi: ")

# Prediksi hasil untuk file yang dimasukkan
result = predict(file_path)

# Menampilkan hasil prediksi
print("Hasil Prediksi (Valid/Fraud):")
print(result[['TransactionID', 'Prediction']])

# Menyimpan hasil prediksi ke file baru
result.to_csv('predictions.csv', index=False)
print("Hasil prediksi telah disimpan ke 'predictions.csv'.")
