import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import date, timedelta

st.set_page_config(page_title="Live NIFTY50 Dashboard", layout="wide")

# ---------------- Stock List ----------------
nifty50_stocks = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","SBIN.NS","BHARTIARTL.NS",
    "HINDUNILVR.NS","ITC.NS","KOTAKBANK.NS","LT.NS","AXISBANK.NS","ASIANPAINT.NS","MARUTI.NS",
    "SUNPHARMA.NS","HCLTECH.NS","ULTRACEMCO.NS","WIPRO.NS","ONGC.NS","POWERGRID.NS","NTPC.NS",
    "BAJAJFINSV.NS","BAJFINANCE.NS","HDFCLIFE.NS","TITAN.NS","JSWSTEEL.NS","ADANIENT.NS",
    "ADANIPORTS.NS","CIPLA.NS","DRREDDY.NS","BRITANNIA.NS","COALINDIA.NS","GRASIM.NS","HINDALCO.NS",
    "DIVISLAB.NS","TECHM.NS","M&M.NS","TATASTEEL.NS","TATAMOTORS.NS","HEROMOTOCO.NS","EICHERMOT.NS",
    "NESTLEIND.NS","BPCL.NS","INDUSINDBK.NS","SHREECEM.NS","SBILIFE.NS","BAJAJ-AUTO.NS",
    "UPL.NS","APOLLOHOSP.NS","HDFCAMC.NS"
]

# ---------------- Date Range ----------------
end = date.today()
start = end - timedelta(days=365*2)  # last 2 years

# ---------------- Sidebar ----------------
st.sidebar.header("Dashboard Options")
option = st.sidebar.radio("Choose analysis:", ["Single Stock", "Multi-Stock Comparison", "Correlation Heatmap"])

# ---------------- Fetch Data ----------------
@st.cache_data
def load_data(tickers, start, end):
    df = yf.download(tickers, start=start, end=end)["Close"]
    return df

df = load_data(nifty50_stocks, start, end)

# ---------------- Single Stock ----------------
if option == "Single Stock":
    stock = st.selectbox("Choose a stock", nifty50_stocks)
    st.subheader(f"📈 Price Trend - {stock}")

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df[stock], label=f"{stock} Close Price", color="blue")
    ax.plot(df.index, df[stock].rolling(50).mean(), label="50-day MA", color="orange")
    ax.plot(df.index, df[stock].rolling(200).mean(), label="200-day MA", color="red")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("Latest Data")
    st.dataframe(df[[stock]].tail(20))

# ---------------- Multi-Stock Comparison ----------------
elif option == "Multi-Stock Comparison":
    stocks = st.multiselect("Choose up to 5 stocks", nifty50_stocks, default=["RELIANCE.NS","INFY.NS"])
    if stocks:
        st.subheader(f"📊 Multi-Stock Comparison")
        fig, ax = plt.subplots(figsize=(12,6))
        for s in stocks:
            ax.plot(df.index, df[s], label=s)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# ---------------- Correlation Heatmap ----------------
elif option == "Correlation Heatmap":
    st.subheader("🔗 Correlation Heatmap - NIFTY50 Stocks")
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(14,10))
    sns.heatmap(corr, cmap="coolwarm", ax=ax, cbar=True)
    st.pyplot(fig)
