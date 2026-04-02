import streamlit as st

from backend.data_manager import POPULAR_STOCKS
from backend.news_ai import fetch_stock_news


def render_stock_news():
    st.markdown("<h2 style='text-align: center;'>📰 Stock News</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>Select a stock to view top 10 latest news with source links.</p>",
        unsafe_allow_html=True,
    )

    selected_stock = st.selectbox("Select stock", options=[""] + POPULAR_STOCKS, index=0, key="news_select")
    chosen_stock = selected_stock.strip().upper()

    if chosen_stock:
        with st.spinner(f"Fetching latest news for {chosen_stock}..."):
            normalized_ticker, news_items = fetch_stock_news(chosen_stock, limit=10)

        if news_items:
            st.success(f"✓ Showing top {min(10, len(news_items))} headlines for **{normalized_ticker}**")

            for i, item in enumerate(news_items[:10], start=1):
                link_text = item["title"].replace("[", "").replace("]", "")
                if item["url"]:
                    st.markdown(
                        f"**{i}. [{link_text}]({item['url']})**  \nSource: {item['source']} | Published: {item['published_at']}"
                    )
                else:
                    st.markdown(f"**{i}. {link_text}**  \nSource: {item['source']} | Published: {item['published_at']}")

            st.info("News data source: Yahoo Finance feed via yfinance. For education only, not financial advice.")
        else:
            st.warning(f"No recent news found for **{chosen_stock}**. Try another ticker.")
    else:
        st.info("👉 Please select a stock to view news.")
