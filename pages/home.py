import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Home", page_icon="📈")

st.markdown("# Home")
st.sidebar.header("Home")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)
