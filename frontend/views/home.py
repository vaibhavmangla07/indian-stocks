import streamlit as st

from src.data_manager import fetch_indices, fetch_data, predict_horizons, POPULAR_STOCKS

def render_home():
    st.markdown("<h3 style='text-align: center;'>📊 Market Overview</h3>", unsafe_allow_html=True)
    with st.spinner("Fetching Market Indices..."):
        indices_data = fetch_indices()

    if indices_data:
        _, col1, col2, col3, _ = st.columns([1, 2, 2, 2, 1])
        cols = [col1, col2, col3]
        for idx, (name, metrics) in enumerate(indices_data.items()):
            with cols[idx]:
                if metrics:
                    st.metric(
                        label=f"**{name}**",
                        value=f"₹{metrics['price']:,.2f}",
                        delta=f"{metrics['change']:,.2f} ({metrics['change_percent']:.2f}%)",
                        delta_color="normal",
                    )
                else:
                    st.metric(label=f"**{name}**", value="Data Unavailable")

    st.divider()

    st.markdown("### 🔍 Stock Explorer")
    control_col1, control_col2 = st.columns([2, 1])
    with control_col1:
        search_term = st.selectbox(
            "Search Stock (Name/Ticker)",
            options=POPULAR_STOCKS,
            index=0,
            help="Select or type a company name like RELIANCE, TCS.",
            key="home_stock_select",
        )
    with control_col2:
        period = st.selectbox(
            "Select Time Period",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3,
            key="home_period_select",
        )

    query = search_term.upper()

    if query:
        ticker = query.upper().strip()
        if not ticker.endswith(".NS") and not ticker.endswith(".BO") and not ticker.startswith("^"):
            ticker = f"{ticker}.NS"

        with st.spinner(f"Analyzing {ticker} data..."):
            df = fetch_data(ticker, period)

        if df is not None and not df.empty:
            st.markdown(f"## 🎯 Asset Analysis: **{ticker}**")

            current_price = df["Close"].iloc[-1]
            mean_price = df["Close"].mean()
            max_price = df["Close"].max()
            min_price = df["Close"].min()
            volatility = df["Close"].std()

            tab1, tab2, tab3 = st.tabs(["📋 Quick Overview", "📈 Price Action & Volume", "🤖 ML Forecast"])

            with tab1:
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Current Price", f"₹{current_price:,.2f}")
                col2.metric("Average Price", f"₹{mean_price:,.2f}")
                col3.metric("Max Price", f"₹{max_price:,.2f}")
                col4.metric("Low Price", f"₹{min_price:,.2f}")
                col5.metric("Volatility Index", f"₹{volatility:,.2f}")

                with st.expander("Show Raw Dataset"):
                    raw_df = df.sort_values(by="Date", ascending=False).head(50)
                    raw_df = raw_df.drop(columns=[col for col in ["Dividends", "Stock Splits"] if col in raw_df.columns])
                    st.dataframe(raw_df, width="stretch")

            with tab2:
                chart_data = df.set_index("Date")[["Close"]]
                st.line_chart(chart_data, width="stretch", color="#1E88E5")

                if "Volume" in df.columns:
                    vol_data = df.set_index("Date")[["Volume"]]
                    st.bar_chart(vol_data, width="stretch", color="#FFA726")

            with tab3:
                pred_short, pred_long = predict_horizons(df)

                if pred_short and pred_long:
                    col_s, col_l = st.columns(2)
                    with col_s:
                        st.success(f"### Short-Term (1-2 Weeks)\n**₹{pred_short:,.2f}**")
                        diff_s = pred_short - current_price
                        st.metric(
                            "Expected Change",
                            f"₹{pred_short:,.2f}",
                            f"₹{diff_s:,.2f} ({diff_s/current_price*100:.2f}%)",
                        )
                    with col_l:
                        st.info(f"### Long-Term (1-3 Years)\n**₹{pred_long:,.2f}**")
                        diff_l = pred_long - current_price
                        st.metric(
                            "Expected Change",
                            f"₹{pred_long:,.2f}",
                            f"₹{diff_l:,.2f} ({diff_l/current_price*100:.2f}%)",
                        )

                    st.divider()
                    st.markdown(
                        """
                    **Model Architecture Details:**
                    - **Algorithm**: `Ridge Regression (Scale-Invariant)`
                    - **Features**: `Price Momentum (5d, 20d, 60d) + Volatility (20d)`
                    - **Objective**: `Dual Horizon Forecasting (10 days & 250 days)`

                    *Note: Professional Statistical Estimation. Not financial advice.*
                    """
                    )
                else:
                    st.warning(
                        "Prediction model requires at least 60 days of historical data. Please ensure your selected period is > 3mo."
                    )
        else:
            st.error(f"Could not fetch data for {ticker}. Ensure it is a valid Yahoo Finance ticker.")
