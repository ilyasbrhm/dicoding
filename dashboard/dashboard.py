import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dashboard/all_data.csv")

df['dteday'] = pd.to_datetime(df['dteday'])

season_mapping_reverse = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
if df['season_hour'].dtype == 'object':
    df['season_hour'] = df['season_hour'].map(season_mapping_reverse)

df['season_hour'] = pd.to_numeric(df['season_hour'], errors='coerce').fillna(0).astype(int)

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter', 0: 'Unknown'}
df['season_label'] = df['season_hour'].map(season_mapping)

st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
end_date = st.sidebar.date_input("End Date", df['dteday'].max())
selected_season = st.sidebar.selectbox("Pilih Musim", df['season_label'].unique())

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]
filtered_df = filtered_df[filtered_df['season_label'] == selected_season]

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    st.title("📊 Bike Sharing Dashboard")

    total_rentals = filtered_df['cnt_day'].sum()
    st.metric("Total Rentals", value=total_rentals)

    st.subheader("Faktor yang Berpengaruh Terhadap Jumlah Penyewaan Sepeda")

    factors = ['hr', 'weathersit_day'] 

    if all(factor in filtered_df.columns for factor in factors):
        hourly_rentals = filtered_df.groupby('hr')['cnt_day'].mean()

        plt.figure(figsize=(10, 5))
        sns.lineplot(x=hourly_rentals.index, y=hourly_rentals.values, marker="o", color="red")
        plt.title("Tren Penyewaan Sepeda Berdasarkan Jam")
        plt.xlabel("Jam (0 - 23)")
        plt.ylabel("Rata-rata Penyewaan Sepeda")
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.warning("Kolom 'hr' atau 'weathersit_day' tidak ditemukan dalam dataset. Pastikan dataset memiliki kolom tersebut.")

    st.subheader("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
if 'weathersit_day' in filtered_df.columns:
    weather_rentals = filtered_df.groupby('weathersit_day')['cnt_day'].mean()

    plt.figure(figsize=(7, 7))
    plt.pie(weather_rentals, labels=weather_rentals.index, autopct='%1.1f%%', colors=["skyblue", "gray", "red", "black"])
    plt.title("Distribusi Penyewaan Sepeda Berdasarkan Cuaca")
    st.pyplot(plt)
else:
    st.warning("Kolom 'weathersit_day' tidak ditemukan dalam dataset. Pastikan dataset memiliki kolom tersebut.")

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

st.caption("Data Source: Bike Sharing Dataset")
