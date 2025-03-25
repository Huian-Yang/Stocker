import yfinance as yf
import pandas as pd
import streamlit as st

def get_shares_outstanding(ticker):
    try:
        return yf.Ticker(ticker).info.get("sharesOutstanding")
    except:
        return None

def get_static_market_cap(ticker):
    try:
        return yf.Ticker(ticker).info.get("marketCap")
    except:
        return None

def get_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.error(f"No data returned for {ticker}.")
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index() 
    data["Ticker"] = ticker

    shares = get_shares_outstanding(ticker)
    data["Estimated Market Cap"] = data["Close"] * shares if shares else None

    return data
