import streamlit as st

from backend.data_manager import fetch_shareholding_pattern, fetch_stock_fundamentals, POPULAR_STOCKS


def _format_decimal(value, digits=2):
    if isinstance(value, (int, float)):
        return f"{float(value):,.{digits}f}"
    return str(value) if value is not None else "N/A"


def _format_percent(value, digits=2):
    if isinstance(value, (int, float)):
        return f"{float(value):.{digits}f}%"
    return str(value) if value is not None else "N/A"


def _format_indian_number(value: int) -> str:
    s = str(int(value))
    if len(s) <= 3:
        return s

    last_three = s[-3:]
    remaining = s[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    return ",".join(parts + [last_three])


def _format_market_cap_display(value):
    if isinstance(value, str) and value.endswith("Cr"):
        return value
    if isinstance(value, (int, float)):
        cr = round(float(value) / 1e7)
        if cr > 0:
            return f"{_format_indian_number(cr)}Cr"
    return str(value) if value is not None else "N/A"


def render_stock_detail():
    st.markdown("<h2 style='text-align: center;'>🏢 Stock Detail</h2>", unsafe_allow_html=True)

    st.markdown(
        """
    <style>
        .detail-banner {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.22), rgba(34, 197, 94, 0.12));
            border: 1px solid rgba(74, 222, 128, 0.35);
            border-radius: 14px;
            padding: 12px 16px;
            font-weight: 700;
            margin-bottom: 14px;
            color: #4ade80;
        }
        .detail-card {
            background: linear-gradient(180deg, rgba(148, 163, 184, 0.08), rgba(30, 41, 59, 0.14));
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 14px;
            padding: 14px 16px;
            min-height: 96px;
        }
        .detail-label {
            font-size: 0.95rem;
            color: #a7b0bf;
            margin-bottom: 6px;
        }
        .detail-value {
            font-size: 2.1rem;
            font-weight: 700;
            color: #f3f4f6;
            line-height: 1.1;
            letter-spacing: -0.3px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    selected_stock = st.selectbox("Select stock", options=[""] + POPULAR_STOCKS, index=0, key="stock_detail_select")
    chosen_stock = selected_stock.strip().upper()

    if chosen_stock:
        if not chosen_stock.endswith(".NS") and not chosen_stock.endswith(".BO") and not chosen_stock.startswith("^"):
            ticker = f"{chosen_stock}.NS"
        else:
            ticker = chosen_stock

        with st.spinner(f"Fetching details for {ticker}..."):
            fundamentals = fetch_stock_fundamentals(ticker)
            shareholding, quarter_info = fetch_shareholding_pattern(ticker)

        if fundamentals:
            pe_display = _format_decimal(fundamentals.get("pe_ratio"))
            book_display = _format_decimal(fundamentals.get("book_value"))
            year_return_display = _format_percent(fundamentals.get("year_return"))
            dividend_display = _format_percent(fundamentals.get("dividend_yield"))
            market_cap_display = _format_market_cap_display(fundamentals.get("market_cap"))
            sector_display = str(fundamentals.get("sector") or "N/A")

            st.markdown(f"<div class='detail-banner'>{ticker} Fundamentals</div>", unsafe_allow_html=True)

            metric_cols = st.columns(2)
            with metric_cols[0]:
                st.markdown(
                    f"<div class='detail-card'><div class='detail-label'>PE Ratio</div><div class='detail-value'>{pe_display}</div></div>",
                    unsafe_allow_html=True,
                )
            with metric_cols[1]:
                st.markdown(
                    f"<div class='detail-card'><div class='detail-label'>Book Value</div><div class='detail-value'>{book_display}</div></div>",
                    unsafe_allow_html=True,
                )

            metric_cols2 = st.columns(4)
            with metric_cols2[0]:
                st.markdown(
                    f"<div class='detail-card'><div class='detail-label'>1-Year Return</div><div class='detail-value'>{year_return_display}</div></div>",
                    unsafe_allow_html=True,
                )
            with metric_cols2[1]:
                st.markdown(
                    f"<div class='detail-card'><div class='detail-label'>Sector</div><div class='detail-value'>{sector_display}</div></div>",
                    unsafe_allow_html=True,
                )
            with metric_cols2[2]:
                st.markdown(
                    f"<div class='detail-card'><div class='detail-label'>Dividend Yield</div><div class='detail-value'>{dividend_display}</div></div>",
                    unsafe_allow_html=True,
                )
            with metric_cols2[3]:
                st.markdown(
                    f"<div class='detail-card'><div class='detail-label'>Market Cap</div><div class='detail-value'>{market_cap_display}</div></div>",
                    unsafe_allow_html=True,
                )

            st.divider()

            if shareholding:
                st.markdown(f"### 📊 Shareholding Pattern {quarter_info['arrow']}")
                st.caption(f"Q: {quarter_info['quarter']} | Date: {quarter_info['date']}")

                import plotly.graph_objects as go

                labels = list(shareholding.keys())
                values = list(shareholding.values())

                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=labels,
                            values=values,
                            hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
                            marker=dict(
                                colors=[
                                    "#1f77b4",
                                    "#ff7f0e",
                                    "#2ca02c",
                                    "#d62728",
                                    "#9467bd",
                                    "#8c564b",
                                ]
                            ),
                        )
                    ]
                )

                fig.update_layout(title="", height=500, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.info("Shareholding data is for reference. For latest accurate data, refer to official stock exchange or company filings.")
        else:
            st.error(f"Could not fetch fundamentals for {ticker}. Ensure it is a valid ticker.")
    else:
        st.info("👉 Please select a stock to view details.")
