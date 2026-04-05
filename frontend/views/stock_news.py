import streamlit as st

from src.data_manager import POPULAR_STOCKS
from src.news_ai import fetch_ai_stock_news


def render_stock_news():
    st.markdown("<h2 style='text-align: center;'>📰 Stock News</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>Select a stock to view the top 10 market news items. Simple tags like deal, current affairs, and latest are added for readability.</p>",
        unsafe_allow_html=True,
    )

    selected_stock = st.selectbox("Select stock", options=[""] + POPULAR_STOCKS, index=0, key="news_select")
    chosen_stock = selected_stock.strip().upper()

    if chosen_stock:
        with st.spinner(f"Fetching news for {chosen_stock}..."):
            normalized_ticker, news_items, ai_summary, used_ai = fetch_ai_stock_news(chosen_stock, limit=10)

        if news_items:
            if used_ai:
                st.success(f"Showing Ollama top {min(10, len(news_items))} headlines for **{normalized_ticker}**")
            else:
                st.warning(f"Showing latest market news for **{normalized_ticker}**")

            if ai_summary:
                st.info(ai_summary)

            for i, item in enumerate(news_items[:10], start=1):
                link_text = item["title"].replace("[", "").replace("]", "")
                item_summary = item.get("summary", "").strip()
                item_category = item.get("category", "latest").strip().replace("_", " ").title()
                metadata_line = f"Source: {item['source']} | Published: {item['published_at']}"
                metadata_line = f"{metadata_line} | Category: {item_category}"

                if item["url"]:
                    st.markdown(f"**{i}. [{link_text}]({item['url']})**")
                else:
                    st.markdown(f"**{i}. {link_text}**")

                if item_summary:
                    st.write(item_summary)

                st.caption(metadata_line)

            st.info("For education only, not financial advice.")
        else:
            st.warning(f"No recent news found for **{chosen_stock}**. Try another ticker.")
    else:
        st.info("👉 Please select a stock to view news.")
