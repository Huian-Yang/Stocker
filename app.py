import streamlit as st
from data_utils import get_data, get_static_market_cap
from cerebras_utils import get_ai_analysis
from plots import plot_prices, plot_market_cap
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Stock Comparison Dashboard with Market Cap Metrics, Growth & AI Analysis")

ticker1 = st.text_input("Enter first stock ticker", value="AAPL")
ticker2 = st.text_input("Enter second stock ticker (optional)", value="")
start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2022-12-31"))

data_frames = []


if st.button("Get Stock Data"):
    data1 = get_data(ticker1, start_date, end_date)
    if data1 is not None:
        data_frames.append(data1)

    if ticker2:
        data2 = get_data(ticker2, start_date, end_date)
        if data2 is not None:
            data_frames.append(data2)

    st.subheader("Static Market Capitalization Metrics")
    col1, col2 = st.columns(2)
    market_cap1 = get_static_market_cap(ticker1)
    with col1:
        st.metric(f"{ticker1} Market Cap", f"${market_cap1:,}" if market_cap1 else "N/A")
    if ticker2:
        market_cap2 = get_static_market_cap(ticker2)
        with col2:
            st.metric(f"{ticker2} Market Cap", f"${market_cap2:,}" if market_cap2 else "N/A")

    if data_frames:
        combined_data = pd.concat(data_frames, ignore_index=True)

        if isinstance(combined_data.columns, pd.MultiIndex):
            combined_data.columns = [' '.join(col).strip() for col in combined_data.columns]

        st.plotly_chart(plot_prices(combined_data), use_container_width=True)

        if combined_data["Estimated Market Cap"].notna().any():
            st.plotly_chart(plot_market_cap(combined_data), use_container_width=True)
        else:
            st.warning("Shares outstanding data unavailable; estimated market cap cannot be computed.")

if st.button("Get AI Analysis"):
    st.subheader("AI Analysis Response")
    response = get_ai_analysis(ticker1, ticker2)
    st.text_area("Response", value=response, height=200)
