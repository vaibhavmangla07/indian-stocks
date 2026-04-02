import datetime
import os

import streamlit as st

from src.logger import logging


def render_contact():
    st.markdown("<h2 style='text-align: center;'>Contact Us</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>We'd love to hear from you. Fill out the form below to get in touch!</p>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        with st.form("contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            message = st.text_area("Message")
            submitted = st.form_submit_button("Send Message")
            if submitted:
                if name and email and message:
                    base_msg_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "messages")
                    os.makedirs(base_msg_dir, exist_ok=True)

                    dt_string = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    msg_folder = os.path.join(base_msg_dir, dt_string)
                    os.makedirs(msg_folder, exist_ok=True)

                    with open(os.path.join(msg_folder, "message.txt"), "w") as f:
                        f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n")

                    logging.info("Contact form submitted by %s <%s>", name, email)
                    st.success(f"Thank you, {name}! Your message has been safely saved.")
                else:
                    st.error("Please fill out all fields to submit.")
