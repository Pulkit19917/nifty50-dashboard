import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filter Options")

# Multiple stock selection
tickers = st.sidebar.multiselect(
    "Select Stocks",
    options=["NSEI", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"],
    default=["NSEI"]
)

# Date range picker
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Timeframe selector
timeframe = st.sidebar.selectbox(
    "Select Timeframe",
    ("Daily", "Weekly", "Monthly")
)

# Technical Indicators
st.sidebar.header("Technical Indicators")
show_sma = st.sidebar.checkbox("SMA (20-day)", value=True)
show_ema = st.sidebar.checkbox("EMA (20-day)", value=False)
show_rsi = st.sidebar.checkbox("RSI (14)", value=False)

# ---------------------------
# Function for Indicators
# ---------------------------
def add_indicators(df):
    if show_sma:
        df["SMA20"] = df["Close"].rolling(window=20).mean()
    if show_ema:
        df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    if show_rsi:
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
    return df

# ---------------------------
# Load & Process Data
# ---------------------------
all_data = {}

for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)

    # Resample based on timeframe
    if timeframe == "Weekly":
        df = df.resample("W").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })
    elif timeframe == "Monthly":
        df = df.resample("M").agg({
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Volume": "sum"
        })

    df = add_indicators(df)
    all_data[ticker] = df

# ---------------------------
# Candlestick + Volume Chart
# ---------------------------
for ticker, df in all_data.items():
    st.subheader(f"{ticker} Stock Chart ({timeframe})")

    fig = go.Figure()

    # Candlesticks
    fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='Candlestick'
)])


    # SMA
    if show_sma and "SMA20" in df:
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA20"], mode="lines", name="SMA20", line=dict(color="blue")))

    # EMA
    if show_ema and "EMA20" in df:
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], mode="lines", name="EMA20", line=dict(color="orange")))

    # Volume Bars
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        name="Volume",
        marker_color="gray",
        opacity=0.3,
        yaxis="y2"
    ))

    # Layout with 2 y-axes
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=700,
        yaxis=dict(title="Price"),
        yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# RSI Chart
# ---------------------------
if show_rsi:
    for ticker, df in all_data.items():
        st.subheader(f"{ticker} RSI (14)")
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", name="RSI", line=dict(color="purple")))
        rsi_fig.add_hline(y=70, line_dash="dot", line_color="red")
        rsi_fig.add_hline(y=30, line_dash="dot", line_color="green")
        rsi_fig.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(rsi_fig, use_container_width=True)

# ---------------------------
# Show Data
# ---------------------------
for ticker, df in all_data.items():
    st.subheader(f"Data for {ticker}")
    st.dataframe(df.tail(20))
