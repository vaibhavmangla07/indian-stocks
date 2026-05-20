import os
import sys

import streamlit as st

# Add project root to path for backend imports inside page modules.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logger import logging

from views.about import render_about
from views.contact import render_contact
from views.home import render_home
from views.stock_detail import render_stock_detail
from views.stock_news import render_stock_news

st.set_page_config(page_title="Stocksy", page_icon="📈", layout="wide")
logging.info("Streamlit app initialized")

st.markdown(
    """
<style>
    .main-header {
        font-size: 5.6rem;
        font-weight: 800;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #757575;
        text-align: center;
        margin-bottom: 20px;
    }
    div.row-widget.stRadio > div {
        display: flex;
        justify-content: center;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div style="font-size: 3rem; font-weight: 800; text-align: center; margin-bottom: 0px; line-height: 1.2;">📈 <span style="background: linear-gradient(to right, #FF3333, #1E88E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Stocksy</span> 📉</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size: 0.8rem; color: #757575; text-align: center; margin-bottom: 20px;">Advanced Market Analysis & Machine Learning Predictions</div>', unsafe_allow_html=True)

menu = st.radio(
    "Main navigation",
    ["Home", "Stock News", "Stock Detail", "About", "Contact Us"],
    horizontal=True,
    index=0,
    label_visibility="collapsed",
)
st.divider()
logging.info("User opened menu tab: %s", menu)

if menu == "Home":
    render_home()
elif menu == "Stock News":
    render_stock_news()
elif menu == "Stock Detail":
    render_stock_detail()
elif menu == "About":
    render_about()
elif menu == "Contact Us":
    render_contact()
