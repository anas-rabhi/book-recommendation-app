import streamlit as st
import numpy as np
import pandas as pd

data = pd.read_csv('./data/books.csv')

st.sidebar.image(data.image_url[0])

k = st.container()

fr, sc = k.columns(2)


#with st.expander('Notez les films :'):


fr.image(data.image_url[0], caption = data.original_title[0])
x = sc.slider(f'Rate {data.original_title[0]}', 1, 5)
if x == 1: sc.markdown("""<div style="text-align: center"> ⭐ </div>""", unsafe_allow_html=True)
if x == 2: sc.markdown("""<div style="text-align: center"> ⭐⭐ </div>""", unsafe_allow_html=True)
if x == 3: sc.markdown("""<div style="text-align: center"> ⭐⭐⭐ </div>""", unsafe_allow_html=True)
if x == 4: sc.markdown("""<div style="text-align: center"> ⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
if x == 5: sc.markdown("""<div style="text-align: center"> ⭐⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)

#k2 = st.container()
#k2.slider()
