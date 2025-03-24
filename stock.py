import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Load environment variables (make sure your .env file has CEREBRAS_API_KEY defined)
load_dotenv()

st.title("Stock Comparison Dashboard with Market Cap Metrics, Growth & AI Analysis")

# Input for tickers (second ticker is optional)
ticker1 = st.text_input("Enter first stock ticker", value="AAPL")
ticker2 = st.text_input("Enter second stock ticker (optional)", value="")

start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2022-12-31"))

# Button to get stock data and plots
if st.button("Get Stock Data"):
    data_frames = []
    
    # Function to retrieve shares outstanding from ticker info
    def get_shares_outstanding(ticker):
        tkr = yf.Ticker(ticker)
        info = tkr.info
        return info.get("sharesOutstanding")
    
    # Function to retrieve static market cap from ticker info
    def get_static_market_cap(ticker):
        tkr = yf.Ticker(ticker)
        info = tkr.info
        return info.get("marketCap")
    
    # Function to fetch and process data for a given ticker
    def get_data(ticker):
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.error(f"No data returned for {ticker}. Please check the ticker or date range.")
            return None
        # Flatten columns if they're multi-indexed
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(level=1)
        data["Ticker"] = ticker
        data["Date"] = data.index
        
        # Calculate estimated market cap: Close * shares outstanding
        shares = get_shares_outstanding(ticker)
        if shares:
            data["Estimated Market Cap"] = data["Close"] * shares
        else:
            data["Estimated Market Cap"] = None
        return data

    # Retrieve data for the first ticker
    data1 = get_data(ticker1)
    if data1 is not None:
        data_frames.append(data1)
        # st.subheader(f"Raw Data for {ticker1}")
        # st.write(data1.head())

    # Retrieve data for the second ticker if provided
    if ticker2:
        data2 = get_data(ticker2)
        if data2 is not None:
            data_frames.append(data2)
            # st.subheader(f"Raw Data for {ticker2}")
            # st.write(data2.head())
    
    # Display static Market Cap metrics using yfinance info
    st.subheader("Static Market Capitalization Metrics")
    col1, col2 = st.columns(2)
    market_cap1 = get_static_market_cap(ticker1)
    with col1:
        st.metric(
            label=f"{ticker1} Market Cap",
            value=f"${market_cap1:,}" if market_cap1 else "N/A"
        )
    if ticker2:
        market_cap2 = get_static_market_cap(ticker2)
        with col2:
            st.metric(
                label=f"{ticker2} Market Cap",
                value=f"${market_cap2:,}" if market_cap2 else "N/A"
            )
    
    # Plot comparative closing prices
    if data_frames:
        combined_data = pd.concat(data_frames)
        fig_price = px.line(
            combined_data,
            x="Date",
            y="Close",
            color="Ticker",
            title="Comparative Closing Prices"
        )
        st.plotly_chart(fig_price, use_container_width=True)

        # Plot estimated market cap growth over time
        if combined_data["Estimated Market Cap"].notna().any():
            fig_cap = px.line(
                combined_data,
                x="Date",
                y="Estimated Market Cap",
                color="Ticker",
                title="Estimated Market Cap Growth Over Time",
                labels={"Estimated Market Cap": "Estimated Market Cap (USD)"}
            )
            st.plotly_chart(fig_cap, use_container_width=True)
        else:
            st.warning("Shares outstanding data unavailable; estimated market cap cannot be computed.")

#---------------- Cerebras API Section ----------------#

# Create a Cerebras client using the API key from environment variables
client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))

if st.button("Get AI Analysis"):
    # Dynamically build a prompt based on the provided tickers
    if ticker2:
        prompt = f"Compare {ticker1} and {ticker2} based on their recent performance."
    else:
        prompt = f"Provide an analysis for {ticker1} based on its recent performance."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model="llama3.1-8b",
        )
        # Instead of dictionary-style indexing, use the object's attributes:
        ai_response = chat_completion.choices[0].message.content
    except Exception as e:
        ai_response = f"Error fetching analysis: {e}"
    
    st.subheader("AI Analysis Response")
    st.text_area("Response", value=ai_response, height=200)
