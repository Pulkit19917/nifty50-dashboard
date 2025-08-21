import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="NIFTY50 Dashboard", layout="wide")

# Title
st.title("📊 NIFTY50 Stock Dashboard")

# Upload Excel
uploaded_file = st.file_uploader("Upload your NIFTY50 Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Sidebar options
    st.sidebar.header("Dashboard Options")
    option = st.sidebar.radio("Choose analysis:", ["Single Stock", "Multi-Stock Comparison", "Correlation Heatmap"])

    # ---------------- Single Stock ----------------
    if option == "Single Stock":
        stocks = df.columns.tolist()
        stock = st.selectbox("Choose a stock", stocks)

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

        st.subheader("Stock Data Preview")
        st.dataframe(df[[stock]].tail(20))

    # ---------------- Multi-Stock Comparison ----------------
    elif option == "Multi-Stock Comparison":
        stocks = st.multiselect("Choose up to 5 stocks to compare", df.columns.tolist(), default=["RELIANCE.NS","INFY.NS"])
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

else:
    st.info("👆 Upload your NIFTY50 Excel file to get started")
