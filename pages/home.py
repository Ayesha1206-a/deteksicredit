import streamlit as st

st.title("RINGKASAN")
st.write("""
    Aplikasi ini dapat memprediksi apakah transaksi kartu kredit merupakan transaksi palsu atau tidak.
    Silakan pilih halaman untuk mengunggah data, visualisasi, atau melakukan prediksi. Mengunggah data digunakan untuk menampilkan data secara keseluruhan. Visualisasi digunakan untuk menampilkan grafik dan juga pengelompokan transaksi. Prediksi digunakan untuk melakukan deteksi akun yang melakukan transaksi anomali dengan standar apabila sebuah akun "v" melakukan transaksi dengan "-" terlalu banyak dan tidak seimbang dengan income maka akun tersebut melalukan anomali
""")
