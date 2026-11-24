import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.title("Apple Stock Candlestick Chart")

# Cache the data so it doesn't reload on every interaction
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv'
    return pd.read_csv(url)

df = load_data()

fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['AAPL.Open'],
    high=df['AAPL.High'],
    low=df['AAPL.Low'],
    close=df['AAPL.Close']
)])

# Render the Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)
