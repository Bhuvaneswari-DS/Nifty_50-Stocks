import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="📈 Stock Analysis Dashboard", layout="wide")


st.title("Welcome to the Stock Analysis Dashboard")

# Database connection config
host = "localhost"
user = "root"
password = "Dataanalyst6889"
port = 3306
database = "stockdata"

# SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Load data from MySQL
@st.cache_data
def load_data():
    return {
        "top_10_volatile_stocks": pd.read_sql("SELECT * FROM top_10_volatile_stocks", engine),
        "top_5_cumulative_stocks": pd.read_sql("SELECT * FROM top_5_cumulative_stocks", engine),
        "stock_price_correlation_matrix": pd.read_sql("SELECT * FROM stock_price_correlation_matrix", engine),
        "sector_performance": pd.read_sql("SELECT * FROM sector_performance", engine),
        "monthly_top_gainers_losers": pd.read_sql("SELECT * FROM monthly_top_gainers_losers", engine),
    }

data = load_data()

# --- Streamlit UI ---


st.markdown("Visualize volatility, performance, gainers/losers, and correlations.")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📉 Volatile Stocks",
    "📈 Cumulative Returns",
    "📊 Correlation Matrix",
    "🏭 Sector Performance",
    "📅 Gainers & Losers"
])

# --- Tab 1: Volatile Stocks ---
with tab1:
    st.subheader("📉 Top 10 Volatile Stocks")
    df = data["top_10_volatile_stocks"]
    df = df.rename(columns={'ticker': 'Stock', 'volatility': 'Volatility'})
    fig = px.bar(df, x="Stock", y="Volatility", color="Volatility", title="Top 10 Volatile Stocks")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# --- Tab 2: Top Cumulative Returns ---
with tab2:
    st.subheader("📈 Top 5 Stocks by Cumulative Returns")
    df = data["top_5_cumulative_stocks"]
    fig = px.bar(df, x="ticker", y="final_cumulative_return", color="ticker", title="Top 5 Cumulative Return Stocks")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# --- Tab 3: Correlation Matrix ---
with tab3:
    st.subheader("📊 Stock Price Correlation Matrix")
    df = data["stock_price_correlation_matrix"]
    df.set_index(df.columns[0], inplace=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.astype(float), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

# --- Tab 4: Sector Performance ---
with tab4:
    st.subheader("🏭 Sector Performance")
    df = data["sector_performance"]
    fig = px.bar(
    df,
    x="sector",
    y="yearly_return",
    color="sector",
    title="Yearly Return by Sector"
)

    st.dataframe(df)

# --- Tab 5: Monthly Gainers & Losers ---
with tab5:
    st.subheader("📅 Monthly Gainers & Losers")
    df = data["monthly_top_gainers_losers"]
    df.columns = df.columns.str.strip().str.lower()


    print("Columns after cleaning:", df.columns.tolist())

# Calculate change_percent only if 'open' and 'close' exist
if 'open' in df.columns and 'close' in df.columns:
    df['change_percent'] = (df['close'] - df['open']) / df['open'] * 100
    df['type'] = df['change_percent'].apply(lambda x: 'Gainer' if x > 0 else 'Loser')
else:
    print("ERROR: 'open' and/or 'close' columns not found.")

    st.markdown("### 📈 Gainers")

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(gainers)

    st.markdown("### 📉 Losers")
    fig_losers = px.bar(Losers, x="Stock", y="Change_Percent", color="Month", title="Top Monthly Losers")
    st.plotly_chart(fig_losers, use_container_width=True)
    st.dataframe(Losers)
