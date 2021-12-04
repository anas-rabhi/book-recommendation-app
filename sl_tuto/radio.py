import streamlit as st
import numpy as np
import pandas as pd

rate = st.radio(
     "Rate the movie",
     ('Not rated', '1', '2', '3', '4', '5'), index=0)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)