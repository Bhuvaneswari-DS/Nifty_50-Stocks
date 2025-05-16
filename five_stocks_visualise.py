import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection details
host = "localhost"
user = "root"
password = "Dataanalyst6889"
port = 3306
database = "stockdata"

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Function to fetch data from MySQL
@st.cache_data
def fetch_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

# Streamlit UI
st.title("📊 Stock Market Analysis Dashboard")

# Sidebar to choose dataset
table_options = ["monthly_top_gainers_losers", "sector_performance",
                 "stock_price_correlation_matrix", "top_5_cumulative_stocks", "top_10_volatile_stocks"]

selected_table = st.sidebar.selectbox("Select Data Table", table_options)
df = fetch_data(selected_table)

# Show data preview
st.subheader(f"Data Preview - {selected_table}")
st.dataframe(df.head())

# Slider for filtering data
if "stock_price" in df.columns:
    min_price, max_price = df["stock_price"].min(), df["stock_price"].max()
    price_filter = st.sidebar.slider("Filter by Stock Price", min_price, max_price, (min_price, max_price))
    df = df[(df["stock_price"] >= price_filter[0]) & (df["stock_price"] <= price_filter[1])]

# Plot graphs based on selected dataset
st.subheader("📈 Data Visualization")

if selected_table == "monthly_top_gainers_losers":
    st.bar_chart(df.set_index("stock_name")["percentage_change"])

elif selected_table == "sector_performance":
    fig, ax = plt.subplots()
    sns.barplot(x="sector", y="performance_index", data=df, ax=ax)
    st.pyplot(fig)

elif selected_table == "stock_price_correlation_matrix":
    fig, ax = plt.subplots()
    sns.heatmap(df.set_index("stock_name").corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

elif selected_table == "top_5_cumulative_stocks":
    st.line_chart(df.set_index("stock_name")["cumulative_returns"])

elif selected_table == "top_10_volatile_stocks":
    fig, ax = plt.subplots()
    sns.boxplot(x="stock_name", y="volatility", data=df, ax=ax)
    st.pyplot(fig)

st.write("✅ **Dashboard Ready! Select different datasets and filters from the sidebar.**")
