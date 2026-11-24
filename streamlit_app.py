import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Candlestick Chart", layout="wide")
st.title("Interactive Candlestick Stock Chart")

ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL").upper()
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp.today())

data = yf.download(ticker, start=start_date, end=end_date, multi_level_index=False)

if not data.empty:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=ticker,
            )
        ]
    )
    fig.update_layout(
        title=f"{ticker} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found for the selected ticker and date range.")
