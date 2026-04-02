import streamlit as st


def render_about():
    st.markdown("<h2 style='text-align: center;'>About Stocksy</h2>", unsafe_allow_html=True)
    st.info(
        "Stocksy is an advanced Streamlit application for analyzing Indian stocks on NSE and BSE. It combines real-time market metrics, historical charting, stock news, fundamentals, and machine learning-based forecasts in one place."
    )

    st.markdown("### Features")
    st.markdown(
        """
    - **Live Market Indices**: Real-time ticker tracking for NIFTY 50, SENSEX, and BANK NIFTY.
    - **Historical Charting**: Comprehensive closing price and volume charts with period filters.
    - **Stock News & Fundamentals**: Top headlines, key financial ratios, and market-cap insights.
    - **Machine Learning Forecasts**: Short-term and long-term price projections.
    """
    )

    st.markdown("### How It Works")
    st.markdown(
        """
    1. The Home page fetches live market data from Yahoo Finance through `yfinance`.
    2. Selected stocks are analyzed using historical price data and lightweight cached computations.
    3. The News page collects the latest headlines for a ticker and shows source links.
    4. The Detail page combines fundamentals and shareholding data into a quick company snapshot.
    5. The Contact page stores each submission locally inside the `messages/` folder.
    """
    )

    st.markdown("### Project Snapshot")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Primary UI", "Streamlit")
    with col2:
        st.metric("Data Source", "Yahoo Finance")
    with col3:
        st.metric("Forecast Models", "2 Trained Models")

    st.markdown("### Note")
    st.warning(
        "The numbers shown here can change with market conditions and API availability. This project is intended for learning and research, not investment advice."
    )
