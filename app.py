import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
st.set_page_config(page_title="📊 Vahan Investor Dashboard", layout="wide")

@st.cache_data
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\naren\Downloads\vahan-investor-dashboard\data\vahan_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()

# -------------------------------
# Dashboard Title
# -------------------------------
st.title("📊 Vahan Investor Dashboard")
st.markdown("This dashboard provides insights from the Vahan dataset.")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filters")

years = df["date"].dt.year.unique()
selected_year = st.sidebar.multiselect("Select Year(s):", years, default=years)

categories = df["category"].unique()
selected_category = st.sidebar.multiselect("Select Vehicle Category:", categories, default=categories)

manufacturers = df["manufacturer"].unique()
selected_manufacturer = st.sidebar.multiselect("Select Manufacturer(s):", manufacturers, default=manufacturers)

# -------------------------------
# Data Filtering
# -------------------------------
filtered_df = df[
    (df["date"].dt.year.isin(selected_year)) &
    (df["category"].isin(selected_category)) &
    (df["manufacturer"].isin(selected_manufacturer))
]

# -------------------------------
# Data Preview
# -------------------------------
st.subheader("🔍 Data Preview")
st.dataframe(filtered_df.head())

# -------------------------------
# Total Registrations Over Time
# -------------------------------
st.subheader("📈 Data Visualizations")

if not filtered_df.empty:
    registrations_over_time = filtered_df.groupby("date")["registrations"].sum().reset_index()
    fig_time = px.line(
        registrations_over_time,
        x="date",
        y="registrations",
        title="Total Registrations Over Time"
    )
    st.plotly_chart(fig_time, use_container_width=True)

    # Registrations by Vehicle Category
    category_counts = (
        filtered_df.groupby("category")["registrations"]
        .sum()
        .reset_index()
        .rename(columns={"category": "Category", "registrations": "Registrations"})
    )
    fig_cat = px.bar(
        category_counts,
        x="Category",
        y="Registrations",
        title="Registrations by Vehicle Category"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # Registrations by Manufacturer
    manu_counts = (
        filtered_df.groupby("manufacturer")["registrations"]
        .sum()
        .reset_index()
        .rename(columns={"manufacturer": "Manufacturer", "registrations": "Registrations"})
    )
    fig_manu = px.bar(
        manu_counts,
        x="Manufacturer",
        y="Registrations",
        title="Registrations by Manufacturer"
    )
    st.plotly_chart(fig_manu, use_container_width=True)

else:
    st.warning("⚠️ No data available for the selected filters.")

# -------------------------------
# Footer
# -------------------------------
st.success("✅ Dashboard loaded successfully!")
