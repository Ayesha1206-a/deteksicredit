import streamlit as st

st.title("RINGKASAN")
st.write("""
    Aplikasi ini dapat memprediksi apakah transaksi kartu kredit merupakan transaksi palsu atau tidak.
    Silakan pilih halaman untuk mengunggah data, visualisasi, atau melakukan prediksi. 
    a. mengunggah data digunakan untuk menampilkan data secara keseluruhan
    b. visualisasi digunakan untuk menampilkan grafik dan juga pengelompokan transaksi 
    c. prediksi digunakan untuk melakukan deteksi akun yang melakukan transaksi anomali dengan standar apabila sebuah akun "v" melakukan transaksi dengan "-" terlalu banyak dan tidak seimbang dengan income maka akun tersebut melalukan anomali
""")
