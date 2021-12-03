import streamlit as st
import numpy as np
import pandas as pd

data = pd.read_csv('./data/books.csv')

rated_books = {}
books_to_rate = {}

def generate_books_to_rate(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data.sort_values('average_rating')
    data = data[data.average_rating.astype(float) > 4]
    data = data.sample(n=20)
    data = data[['title', 'image_url', 'book_id']]
    data['container'] = st.container
    data['Response'] = None
    return data

books = generate_books_to_rate(data)

#for i in books.iterrows():
    #i[1].container
#à revoir

## add bouton to add random books or generate another sample....

## add bouton that takes into account the already watched among recommended movies and do another search

#for i in books.iterrows():




st.sidebar.image(data.image_url[0])

#k = st.container()

#fr, sc = k.columns(2)

d = {}

#with st.expander('Notez les films :'):
with st.container():
    f, s = st.columns(2)

    with f :
        st.image(data.image_url[0], caption = data.original_title[0])
    with s:
        st.text(' ')
        st.text(' ')
        d[f'{data.original_title[0]}'] = st.slider(f'Rate {data.original_title[0]}', 1, 5)
        if d[f'{data.original_title[0]}'] == 1: st.markdown("""<div style="text-align: center"> ⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[0]}'] == 2: st.markdown("""<div style="text-align: center"> ⭐⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[0]}'] == 3: st.markdown("""<div style="text-align: center"> ⭐⭐⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[0]}'] == 4: st.markdown("""<div style="text-align: center"> ⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[0]}'] == 5: st.markdown("""<div style="text-align: center"> ⭐⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)

#k2 = st.container()
#k2.slider()
st.text(data.original_title[0])

with st.container():
    f, s = st.columns(2)

    with f :
        st.image(data.image_url[1], caption = 'data.original_title[1]')
    with s:
        st.text(' ')
        st.text(' ')

        d[f'{data.original_title[1]}'] = st.slider(f'Rate data.original_title[1]', 1, 5)
        if d[f'{data.original_title[1]}'] == 1: st.markdown("""<div style="text-align: center"> ⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[1]}'] == 2: st.markdown("""<div style="text-align: center"> ⭐⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[1]}'] == 3: st.markdown("""<div style="text-align: center"> ⭐⭐⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[1]}'] == 4: st.markdown("""<div style="text-align: center"> ⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
        if d[f'{data.original_title[1]}'] == 5: st.markdown("""<div style="text-align: center"> ⭐⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)