import streamlit as st
import pandas as pd

st.title("Analisis Transaksi Kartu Kredit dengan Prediksi Anomali")

# Unggah file CSV
uploaded_file = st.file_uploader("Unggah file CSV untuk analisis", type="csv")
if uploaded_file:
    try:
        # Membaca file CSV hanya dengan kolom yang dibutuhkan
        data = pd.read_csv(uploaded_file, usecols=['time'] + [col for col in pd.read_csv(uploaded_file, nrows=1).columns if col.startswith('V')])

        # Cek apakah kolom 'time' ada dalam file
        time_column = None
        for col in data.columns:
            if 'time' in col.lower():  # Mencari kolom yang mengandung 'time' tanpa memperhatikan kapitalisasi
                time_column = col
                break

        # Jika tidak ada kolom time ditemukan
        if time_column is None:
            st.error("File CSV tidak mengandung kolom 'time'. Pastikan kolom waktu ada dalam data.")
        else:
            # Menampilkan nama kolom 'time' yang ditemukan
            st.write(f"Kolom waktu yang ditemukan: {time_column}")

            # Ambil kolom yang dimulai dengan 'V' (misalnya V1, V2, ..., Vn)
            v_columns = [col for col in data.columns if col.startswith('V')]  # Kolom yang dimulai dengan 'V'
            if not v_columns:
                st.error("File CSV tidak mengandung kolom yang dimulai dengan 'V'.")
            else:
                # Menampilkan data hanya untuk kolom 'time' dan fitur 'V1-Vn' 
                st.write(f"Menampilkan data untuk kolom '{time_column}' dan fitur V1-Vn:")
                st.dataframe(data[[time_column] + v_columns])

                # Deteksi transaksi dengan nilai negatif terbanyak
                transaction_negative_counts = {}

                # Iterasi untuk setiap 'time' dan hitung jumlah nilai negatif pada kolom V
                for time in data[time_column].unique():
                    time_data = data[data[time_column] == time]
                    negative_counts = (time_data[v_columns] < 0).sum(axis=0)  # Hitung nilai negatif pada setiap fitur V
                    transaction_negative_counts[time] = negative_counts

                # Mencari 'V1-Vn' dengan transaksi negatif terbanyak dalam setiap waktu
                max_negatives_per_time = {}
                for time, negative_counts in transaction_negative_counts.items():
                    max_negative = negative_counts.max()
                    columns_with_max_negatives = negative_counts[negative_counts == max_negative].index.tolist()
                    max_negatives_per_time[time] = {
                        'max_negative': max_negative,
                        'columns': columns_with_max_negatives
                    }

                # Menampilkan hasil analisis dan menandai akun anomali
                for time, analysis in max_negatives_per_time.items():
                    st.write(f"\n**Waktu: {time}**")
                    st.write(f"Jumlah transaksi negatif terbanyak: {analysis['max_negative']}")
                    st.write(f"Fitur V yang memiliki transaksi negatif terbanyak: {', '.join(analysis['columns'])}")

                    # Menandai akun sebagai anomali jika fitur V memiliki transaksi negatif terbanyak
                    for col in analysis['columns']:
                        st.write(f"Akun yang menggunakan {col} dianggap **anomali** pada waktu {time}")

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam memproses file: {e}")
