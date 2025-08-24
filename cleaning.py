import pandas as pd
df = pd.read_csv("crime_dataset_india.csv")
print(df.info())
print("\nMissing Values:\n", df.isnull().sum())
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.drop(columns= ["date_of_occurrence"])
df = df.rename(columns= {"time_of_occurrence" : "date_and_time_of_occurrence"})
date_columns = ["date_reported", "date_and_time_of_occurrence"]
df["date_case_closed"] = df["date_case_closed"].fillna("Not Closed")
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
categorical_cols = ["weapon_used", "crime_domain", "victim_gender", "city", "crime_description", "victim_age"]
for col in categorical_cols:
    df[col] = df[col].fillna("Unknown")
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print("After Cleaning:")
print(df.info())
print("\nMissing Values:\n", df.isnull().sum())
df.to_csv("cleaned_crime_dataset.csv", index=False)
print("\nCleaned dataset saved as 'cleaned_crime_dataset.csv'")