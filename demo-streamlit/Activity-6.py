from datetime import date, timedelta

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# ---------------------------------------------------------------
# Page config
# ---------------------------------------------------------------
st.set_page_config(page_title="Stock dashboard", page_icon="📈", layout="wide")

st.title("Stock dashboard")
st.caption("In-class activity 6 — comparing two tickers with normalized prices")


# ---------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------
@st.cache_data(ttl="1h")
def get_stock_data(ticker: str, start_date: date, end_date: date) -> pd.DataFrame:
    """Download historical price data for a ticker from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    return df


# ---------------------------------------------------------------
# Sidebar inputs
# ---------------------------------------------------------------
with st.sidebar:
    st.header("Inputs")
    ticker = st.text_input("Main ticker", value="AAPL")
    comparison_ticker = st.text_input("Comparison ticker", value="SPY")
    run_button = st.button("Run", type="primary", width="stretch")

# Date range: last 365 days
start = date.today() - timedelta(days=365)
end = date.today()


# ---------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------
if run_button:
    # Fetch data for both tickers using the cached function
    df = get_stock_data(ticker, start, end)
    comparison_df = get_stock_data(comparison_ticker, start, end)

    if df.empty:
        st.error(f"No data found for ticker '{ticker}'. Please check the symbol.")
        st.stop()
    if comparison_df.empty:
        st.error(f"No data found for ticker '{comparison_ticker}'. Please check the symbol.")
        st.stop()

    # -----------------------------------------------------------
    # Part 2: Normalize both tickers to a base of 100
    # -----------------------------------------------------------
    df["normalized_close"] = (df["Close"] / df["Close"].iloc[0]) * 100
    comparison_df["normalized_close"] = (comparison_df["Close"] / comparison_df["Close"].iloc[0]) * 100

    # -----------------------------------------------------------
    # Create tabs
    # -----------------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Chart", "📄 Data", "📋 Statistics", "📈 Comparison"])

    with tab1:
        st.subheader(f"{ticker} closing price")
        st.line_chart(df["Close"])

    with tab2:
        st.subheader(f"{ticker} historical data")
        st.dataframe(df, width="stretch")

    with tab3:
        st.subheader(f"{ticker} summary statistics")
        st.dataframe(df.describe(), width="stretch")

    with tab4:
        st.subheader("Normalized performance comparison")

        # Combine both normalized series into one long-format DataFrame for plotly
        combined = pd.concat(
            [
                pd.DataFrame(
                    {
                        "Date": df.index,
                        "Normalized close": df["normalized_close"].values,
                        "Ticker": ticker,
                    }
                ),
                pd.DataFrame(
                    {
                        "Date": comparison_df.index,
                        "Normalized close": comparison_df["normalized_close"].values,
                        "Ticker": comparison_ticker,
                    }
                ),
            ],
            ignore_index=True,
        )

        fig = px.line(
            combined,
            x="Date",
            y="Normalized close",
            color="Ticker",
            title=f"{ticker} vs {comparison_ticker} Performance (Base 100)",
        )
        st.plotly_chart(fig, width="stretch")

        # Summary statistics for the normalized data
        st.subheader("Summary statistics (base 100)")
        summary = pd.DataFrame(
            {
                "Min": [
                    df["normalized_close"].min(),
                    comparison_df["normalized_close"].min(),
                ],
                "Max": [
                    df["normalized_close"].max(),
                    comparison_df["normalized_close"].max(),
                ],
                "Final normalized value": [
                    df["normalized_close"].iloc[-1],
                    comparison_df["normalized_close"].iloc[-1],
                ],
            },
            index=[ticker, comparison_ticker],
        )
        st.dataframe(summary.round(2), width="stretch")
else:
    st.info("Enter your tickers in the sidebar and press **Run** to load the dashboard.")
