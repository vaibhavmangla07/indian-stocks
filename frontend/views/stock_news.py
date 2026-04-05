import streamlit as st

from src.data_manager import POPULAR_STOCKS
from src.news_ai import fetch_ai_stock_news


@st.cache_data(ttl=300)
def _cached_news(stock_query: str):
    return fetch_ai_stock_news(stock_query, limit=10)


def render_stock_news():
    st.markdown("<h2 style='text-align:center'>📰 Stock News Intelligence</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;color:#757575'>Select a stock to get AI-curated news with market insights.</p>",
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 2, 1])
    with col:
        selected_stock = st.selectbox(
            "Select Stock",
            options=[""] + POPULAR_STOCKS,
            index=0,
            key="news_select",
        )

    if not selected_stock:
        st.info("👉 Select a stock above to load AI news analysis.")
        return

    stock = selected_stock.strip().upper()

    with st.status("🧠 AI is analyzing stock news...", expanded=True) as status:
        st.write("📡 Fetching latest headlines from Google News & Yahoo Finance...")
        ticker, news_items, ai_summary, next_steps, used_ai = _cached_news(stock)
        if used_ai:
            st.write("🤖 Running Ollama AI analysis — picking top headlines & market impact...")
        st.write("✅ Done!")
        status.update(label="Analysis complete!", state="complete", expanded=False)

    if not news_items:
        st.warning(f"No recent news found for **{stock}**. Try another ticker.")
        return

    stock_display = ticker.replace(".NS", "").replace(".BO", "")

    st.markdown("---")
    st.markdown(f"## 📊 Top {len(news_items)} Latest News — **{stock_display}**")

    if ai_summary:
        st.info(f"**AI Overview:** {ai_summary}")

    st.markdown("")

    if used_ai:
        header = "| # | Date | Headline | Why it matters | Source |"
        separator = "|---|------|----------|----------------|--------|"
        rows = [header, separator]

        for i, item in enumerate(news_items, 1):
            title = item.get("title", "Untitled").replace("|", "\\|")
            url = item.get("url", "")
            date = item.get("published_at", "N/A")
            why = item.get("why_it_matters", "—").replace("|", "\\|") or "—"
            source = item.get("source", "Unknown").replace("|", "\\|")

            headline_cell = f"[{title}]({url})" if url else title
            rows.append(f"| {i} | {date} | {headline_cell} | {why} | {source} |")

        st.markdown("\n".join(rows))
    else:
        st.markdown("### Latest Headlines")
        for i, item in enumerate(news_items, 1):
            title = item.get("title", "Untitled")
            url = item.get("url", "")
            source = item.get("source", "Unknown")
            date = item.get("published_at", "N/A")
            category = item.get("category", "latest").replace("_", " ").title()

            if url:
                st.markdown(f"**{i}.** [{title}]({url})")
            else:
                st.markdown(f"**{i}.** {title}")
            st.caption(f"📰 {source} &nbsp;|&nbsp; 🕐 {date} &nbsp;|&nbsp; 🏷 {category}")

    if next_steps:
        st.markdown("---")
        st.markdown("### ✅ Investor Next Steps")
        for i, step in enumerate(next_steps, 1):
            st.markdown(f"**{i}.** {step}")

    st.markdown("---")
    st.caption("⚠️ For educational purposes only. Not financial advice.")
