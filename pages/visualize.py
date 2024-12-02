import streamlit as st
import pandas as pd
import altair as alt

st.title("Visualisasi Data")

uploaded_file = st.file_uploader("Unggah file CSV untuk visualisasi", type="csv")
if uploaded_file:
    # Membaca data
    data = pd.read_csv(uploaded_file)
    st.write("Data yang diunggah:")
    st.dataframe(data.head())
    
    # Menyaring kolom numerik untuk sumbu X dan Y
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) < 2:
        st.warning("Data tidak memiliki cukup kolom numerik untuk grafik.")
    else:
        # Memilih kolom untuk sumbu X dan Y
        x_axis = st.selectbox("Pilih kolom X:", numeric_columns)
        y_axis = st.selectbox("Pilih kolom Y:", numeric_columns)

        # Membuat grafik jika kedua kolom dipilih
        if x_axis and y_axis:
            chart = alt.Chart(data).mark_point().encode(
                x=x_axis,
                y=y_axis,
                tooltip=[x_axis, y_axis]
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
