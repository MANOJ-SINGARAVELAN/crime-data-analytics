import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crime Data Analytics", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_crime_dataset.csv")
    df['date_reported'] = pd.to_datetime(df['date_reported'], errors='coerce')
    df['year'] = df['date_reported'].dt.year
    df['month'] = df['date_reported'].dt.month_name()
    return df
df = load_data()

st.sidebar.header("Filters")

years = sorted(df['year'].dropna().unique())
selected_years = st.sidebar.multiselect("**Select Year**", years, default=years)

months = sorted(df['month'].dropna().unique())
selected_months = st.sidebar.multiselect("**Select Month**", months, default=months)

cities = sorted(df['city'].dropna().unique())
selected_cities = st.sidebar.multiselect("**Select City**", cities, default=cities)

genders = sorted(df['victim_gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("**Select Gender**", genders, default=genders)

filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['city'].isin(selected_cities)) &
    (df["month"].isin(selected_months)) &
    (df['victim_gender'].isin(selected_genders))]

st.title("Crime Data Analytics Dashboard")
st.write(f"**Total Records:** {len(filtered_df)}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Crimes", len(filtered_df))
col2.metric("Unique Cities", filtered_df["city"].nunique())
col3.metric("Unique Crime Domains", filtered_df["crime_domain"].nunique())

st.subheader("Crimes by Year")
year_count = filtered_df.groupby('year').size().reset_index(name='count')
fig1 = px.bar(year_count, x='year', y='count', title="Crimes per Year",  text_auto=True, color='count')
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Crimes by Month")
month_count = filtered_df.groupby('month').size().reset_index(name='count')
fig2 = px.line(month_count, x='month', y='count', markers=True, title="Crimes per Month", text='count')
fig2.update_traces(textposition="top center")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Crimes by Domain")
domain_count = filtered_df['crime_domain'].value_counts().reset_index()
domain_count.columns = ['crime_domain', 'count']
fig3 = px.pie(domain_count, names='crime_domain', values='count', hole=0.3, title="Crime Domain Distribution")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Crimes by Code")
code_count = filtered_df['crime_code'].value_counts().reset_index()
code_count.columns = ['crime_code', 'count']
fig4 = px.bar(code_count, x='count', y='crime_code', orientation='h', title="Crime Codes", text_auto=True)
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Crimes by Description")
desc_count = filtered_df['crime_description'].value_counts().reset_index()
desc_count.columns = ['crime_description', 'count']
fig5 = px.bar(desc_count, x='crime_description', y='count', title="Crime Descriptions", text_auto=True, color='count')
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Crimes by City & Gender")
city_gender_count = filtered_df.groupby(['city', 'victim_gender']).size().reset_index(name='count')
fig6 = px.bar(city_gender_count, x='city', y='count', color='victim_gender', title="Crimes by City and Gender", text='count', barmode='stack')
st.plotly_chart(fig6, use_container_width=True)

st.subheader("Victim Age Distribution")
age_count = filtered_df.groupby('victim_age').size().reset_index(name='count')
fig7 = px.scatter(age_count, x='victim_age', y='count', size='count', color='count', title="Victim Age vs Crime Count", hover_name='victim_age')
st.plotly_chart(fig7, use_container_width=True)

st.subheader("Crimes by Weapon Used")
weapon_count = filtered_df['weapon_used'].value_counts().reset_index()
weapon_count.columns = ['weapon_used', 'count']
fig8 = px.bar(weapon_count, x='weapon_used', y='count', title="Weapon Usage", text_auto=True, color='count')
st.plotly_chart(fig8, use_container_width=True)

st.subheader("Gender Distribution")
gender_count = filtered_df['victim_gender'].value_counts().reset_index()
gender_count.columns = ['victim_gender', 'count']
fig9 = px.pie(gender_count, names='victim_gender', values='count', title="Gender Distribution", hole=0.3)
st.plotly_chart(fig9, use_container_width=True)

st.subheader("Download data in csv format")
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_crime_data.csv",
    mime="text/csv")
