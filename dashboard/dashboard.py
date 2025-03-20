import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

df = day_df.copy()

df['dteday'] = pd.to_datetime(df['dteday'])

season_mapping_reverse = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
df['season'] = df['season'].map(season_mapping_reverse).fillna(df['season']).astype(int)

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter', 0: 'Unknown'}
df['season_label'] = df['season'].map(season_mapping)

st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Start Date", df['dteday'].min())
end_date = st.sidebar.date_input("End Date", df['dteday'].max())
selected_season = st.sidebar.selectbox("Pilih Musim", ['All'] + sorted(df['season_label'].unique()))
selected_weather = st.sidebar.selectbox("Pilih Cuaca", ['All'] + sorted(df['weathersit'].astype(str).unique()))

workingday_mapping = {"All": "All", "Iya": 1, "Tidak": 0}
holiday_mapping = {"All": "All", "Iya": 1, "Tidak": 0}

selected_workingday_label = st.sidebar.selectbox("Hari Kerja", list(workingday_mapping.keys()))
selected_holiday_label = st.sidebar.selectbox("Hari Libur", list(holiday_mapping.keys()))

selected_workingday = workingday_mapping[selected_workingday_label]
selected_holiday = holiday_mapping[selected_holiday_label]

filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season_label'] == selected_season]
if selected_weather != 'All':
    filtered_df = filtered_df[filtered_df['weathersit'].astype(str) == selected_weather]
if selected_workingday != 'All':
    filtered_df = filtered_df[filtered_df['workingday'] == int(selected_workingday)]
if selected_holiday != 'All':
    filtered_df = filtered_df[filtered_df['holiday'] == int(selected_holiday)]

filtered_df = filtered_df.copy()

st.title("📊 Bike Sharing Dashboard")

total_rentals = filtered_df['cnt'].sum()
st.metric("Total Rentals", value=total_rentals)

st.subheader("Faktor yang Berpengaruh Terhadap Jumlah Penyewaan Sepeda")
selected_features = ["temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"]
available_features = [feature for feature in selected_features if feature in filtered_df.columns]

df_selected = filtered_df[available_features]
correlation_matrix = df_selected.corr()
corr_target = correlation_matrix["cnt"].drop("cnt").abs().sort_values(ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x=corr_target.values, y=corr_target.index, palette="viridis")
plt.xlabel("Nilai Korelasi")
plt.ylabel("Fitur")
plt.title("Fitur Paling Berpengaruh terhadap Penyewaan Sepeda")
st.pyplot(plt)

st.subheader("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
weather_avg = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()
plt.figure(figsize=(12, 8))
sns.barplot(x=weather_avg["weathersit"], y=weather_avg["cnt"], palette="coolwarm")
plt.xlabel("Kategori Cuaca")
plt.ylabel("Rata-rata Jumlah Penyewaan Sepeda")
plt.title("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
plt.xticks(ticks=[0, 1, 2, 3], labels=["Clear", "Mist", "Light Rain/Snow", "Heavy Rain/Snow"])
st.pyplot(plt)

st.subheader("Filtered Data")
st.dataframe(filtered_df)

st.caption("Data Source: Bike Sharing Dataset")
