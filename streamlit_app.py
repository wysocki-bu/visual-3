import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Simulated Candlestick Chart", layout="wide")
st.title("Interactive Candlestick Chart (Simulated Data)")

# Sidebar controls
st.sidebar.header("Simulation & Chart Controls")
days = st.sidebar.slider("Number of Trading Days", min_value=30, max_value=365, value=120, step=10)
start_price = st.sidebar.number_input("Starting Price ($)", min_value=1.0, max_value=10000.0, value=150.0, step=5.0)
volatility = st.sidebar.slider("Daily Volatility (%)", min_value=0.5, max_value=8.0, value=2.0, step=0.1) / 100
seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=99999, value=42, step=1)
show_ma = st.sidebar.checkbox("Show Moving Averages (10 & 20)", value=True)


@st.cache_data
def generate_ohlcv_data(num_days: int, initial_price: float, daily_vol: float, random_seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(random_seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=num_days)

    # Random walk with slight upward drift for closing prices
    returns = rng.normal(loc=0.0005, scale=daily_vol, size=num_days)
    close_prices = initial_price * np.cumprod(1 + returns)

    # Open starts near previous close (or initial price on day 1)
    open_prices = np.empty(num_days)
    open_prices[0] = initial_price
    gaps = rng.normal(loc=0.0, scale=daily_vol * 0.4, size=num_days - 1)
    open_prices[1:] = close_prices[:-1] * (1 + gaps)

    # High and Low bound both Open and Close
    wick_high = np.abs(rng.normal(loc=daily_vol * 0.6, scale=daily_vol * 0.4, size=num_days))
    wick_low = np.abs(rng.normal(loc=daily_vol * 0.6, scale=daily_vol * 0.4, size=num_days))

    body_max = np.maximum(open_prices, close_prices)
    body_min = np.minimum(open_prices, close_prices)

    high_prices = body_max * (1 + wick_high)
    low_prices = np.maximum(0.01, body_min * (1 - wick_low))

    volume = rng.integers(low=500_000, high=5_000_000, size=num_days)

    df = pd.DataFrame(
        {
            "Date": dates,
            "Open": np.round(open_prices, 2),
            "High": np.round(high_prices, 2),
            "Low": np.round(low_prices, 2),
            "Close": np.round(close_prices, 2),
            "Volume": volume,
        }
    )
    df["MA_10"] = df["Close"].rolling(window=10).mean()
    df["MA_20"] = df["Close"].rolling(window=20).mean()
    return df


df = generate_ohlcv_data(days, start_price, volatility, int(seed))

# Build interactive Plotly candlestick figure
fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="OHLC",
        )
    ]
)

if show_ma:
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_10"], mode="lines", name="10-Day MA"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_20"], mode="lines", name="20-Day MA"))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price ($)",
    xaxis_rangeslider_visible=False,
    hovermode="x unified",
    height=550,
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("View Simulated OHLCV Data"):
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
