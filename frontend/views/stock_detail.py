import streamlit as st
from backend.data_manager import fetch_stock_fundamentals, POPULAR_STOCKS


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

    selected_stock = st.selectbox("Select stock", options=[""] + POPULAR_STOCKS, index=0, key="stock_detail_select")
    chosen_stock = selected_stock.strip().upper()

    if chosen_stock:
        if not chosen_stock.endswith(".NS") and not chosen_stock.endswith(".BO") and not chosen_stock.startswith("^"):
            ticker = f"{chosen_stock}.NS"
        else:
            ticker = chosen_stock

        with st.spinner(f"Fetching details for {ticker}..."):
            fundamentals = fetch_stock_fundamentals(ticker)

        if fundamentals:
            company_name = str(fundamentals.get("company_name") or ticker)
            summary_display = fundamentals.get("business_summary") or "N/A"

            st.subheader(company_name)

            snapshot_labels = [
                ("Previous Close", fundamentals.get("previous_close")),
                ("Open", fundamentals.get("open_price")),
                ("Day's Range", f"{_format_decimal(fundamentals.get('day_low'))} - {_format_decimal(fundamentals.get('day_high'))}"),
                ("52 Week Range", f"{_format_decimal(fundamentals.get('week_52_low'))} - {_format_decimal(fundamentals.get('week_52_high'))}"),
                ("Market Cap", fundamentals.get("market_cap")),
                ("Beta", fundamentals.get("beta")),
                ("Volume", fundamentals.get("volume")),
                ("Avg. Volume", fundamentals.get("avg_volume")),
            ]

            for start in range(0, len(snapshot_labels), 4):
                row = snapshot_labels[start : start + 4]
                cols = st.columns(len(row))
                for col, (label, value) in zip(cols, row):
                    with col:
                        st.metric(label, _format_market_cap_display(value) if label == "Market Cap" else _format_decimal(value) if label in {"Beta"} else _format_indian_number(value) if label in {"Volume", "Avg. Volume"} and isinstance(value, (int, float)) else str(value))

            st.divider()

            st.markdown("### About")
            st.write(summary_display)

            about_cols = st.columns(2)
            with about_cols[0]:
                st.write(f"**Website:** {fundamentals.get('website') or 'N/A'}")
                st.write(f"**Industry:** {fundamentals.get('industry') or 'N/A'}")
            with about_cols[1]:
                st.write(f"**Employees:** {fundamentals.get('full_time_employees') or 'N/A'}")
                st.write(f"**Fiscal Year End:** {fundamentals.get('fiscal_year_end') or 'N/A'}")

            st.divider()

            st.markdown("### Details")
            detail_cols = st.columns(4)
            detail_values = [
                ("PE Ratio", fundamentals.get("pe_ratio")),
                ("Book Value", fundamentals.get("book_value")),
                ("1-Year Return", fundamentals.get("year_return")),
                ("Dividend Yield", fundamentals.get("dividend_yield")),
            ]
            for column, (label, value) in zip(detail_cols, detail_values):
                with column:
                    st.metric(label, _format_percent(value) if label in {"1-Year Return", "Dividend Yield"} else _format_decimal(value))
        else:
            st.error(f"Could not fetch fundamentals for {ticker}. Ensure it is a valid ticker.")
    else:
        st.info("👉 Please select a stock to view details.")
