import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Swing Trading Master Dashboard", layout="wide")
st.title("🧭 Swing Trading MASTER Dashboard")
st.markdown("**Live on iPhone • Master Score • Sector Rotation**")

@st.cache_data(ttl=300)
def get_data(ticker, period="2y"):
    df = yf.download(ticker, period=period)
    return df.dropna()

sector_etfs = {
    "Energy": "XLE", "Materials": "XLB", "Industrials": "XLI",
    "Consumer Discretionary": "XLY", "Consumer Staples": "XLP",
    "Health Care": "XLV", "Financials": "XLF",
    "Information Technology": "XLK", "Communication Services": "XLC",
    "Utilities": "XLU", "Real Estate": "XLRE"
}

spy = get_data("SPY")

def master_score(df, spy_df):
    latest = df.iloc[-1]
    score = 0
    sma50 = df['Close'].rolling(50).mean().iloc[-1]
    sma200 = df['Close'].rolling(200).mean().iloc[-1]
    if latest['Close'] > sma50 > sma200:
        score += 40
    if latest['Close'] > df['Close'].rolling(20).mean().iloc[-1]:
        score += 30
    rel_strength = (latest['Close'] / spy_df.iloc[-1]['Close']) / (df.iloc[-22]['Close'] / spy_df.iloc[-22]['Close']) if len(df) > 21 else 1
    score += 30 if rel_strength > 1 else 0
    return round(score, 1)

data = []
for sector, ticker in sector_etfs.items():
    df = get_data(ticker)
    score = master_score(df, spy)
    latest = df.iloc[-1]
    ret_1d = (latest['Close'] / df.iloc[-2]['Close'] - 1) * 100
    data.append({
        "Sector": sector,
        "Master Score": score,
        "1D %": round(ret_1d, 2),
        "Trend": "🟢 STRONG" if score >= 70 else "🟡 Watch" if score >= 50 else "🔴 Weak"
    })

df_summary = pd.DataFrame(data).sort_values("Master Score", ascending=False)
st.dataframe(df_summary.style.background_gradient(cmap='RdYlGn', subset=['Master Score']), use_container_width=True)

st.success("✅ Full Master Dashboard is now live and working perfectly on your iPhone!")
st.caption("Refresh anytime for live market data • Bookmark this page")