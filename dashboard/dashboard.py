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
selected_season = st.sidebar.selectbox("Pilih Musim", ['All'] + sorted(df['season_label'].unique()))
selected_weather = st.sidebar.selectbox("Pilih Cuaca", ['All'] + sorted(df['weathersit_day'].astype(str).unique()))
selected_workingday = st.sidebar.selectbox("Hari Kerja", ['All', 0, 1])
selected_holiday = st.sidebar.selectbox("Hari Libur", ['All', 0, 1])

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]
if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season_label'] == selected_season]
if selected_weather != 'All':
    filtered_df = filtered_df[filtered_df['weathersit_day'].astype(str) == selected_weather]
if selected_workingday != 'All':
    filtered_df = filtered_df[filtered_df['workingday_day'] == int(selected_workingday)]
if selected_holiday != 'All':
    filtered_df = filtered_df[filtered_df['holiday_day'] == int(selected_holiday)]

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    st.title("📊 Bike Sharing Dashboard")

    total_rentals = filtered_df['cnt_day'].sum()
    st.metric("Total Rentals", value=total_rentals)

    st.subheader("Faktor yang Berpengaruh Terhadap Jumlah Penyewaan Sepeda")
    features = ["temp_hour", "hum_hour", "windspeed_hour", "hr", "season_hour"]
    available_features = [col for col in features if col in filtered_df.columns]
    
    if available_features:
        plt.figure(figsize=(15, 10))
        for i, col in enumerate(available_features, 1):
            plt.subplot(2, 3, i)
            sns.scatterplot(x=filtered_df[col], y=filtered_df["cnt_day"], alpha=0.5, color="blue")
            plt.title(f"Hubungan {col} dengan Penyewaan Sepeda")
            plt.xlabel(col)
            plt.ylabel("Jumlah Penyewaan Sepeda")
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.warning("Tidak ada fitur yang tersedia dalam dataset untuk analisis faktor penyewaan sepeda.")

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
