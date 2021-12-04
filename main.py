import streamlit as st
import numpy as np
import pandas as pd
from book_app import BookDisplay
data = pd.read_csv('./data/books.csv')

st.sidebar.write(
    "Recommanded movies")

if 'number_of_books' not in st.session_state:
    st.session_state['number_of_books'] = 5

if 'random_books' not in st.session_state:
    st.session_state['random_books'] = 440

if 'rated_books' not in st.session_state:
    st.session_state['rated_books'] = {}




search = st.text_input('Search a book by its title')


f, s = st.columns(2)




books_to_display, nb = BookDisplay.generate_books_to_rate(data, number_of_books=st.session_state['number_of_books'], rstate=st.session_state['random_books'], search=search)


st.write(f'Number of books available : {nb}')
st.write(f'Number of books displayed : {st.session_state["number_of_books"]}')
st.write(f'__________')

st.title(f'Books to rate')

BookDisplay.display_books_to_rate(books_to_display, st.session_state['rated_books'])

with f:
    if st.button('Load more books'):
        st.session_state['number_of_books'] += 5
with s:
    if st.button('Show another sample of books'):
        st.session_state['random_books'] += 5
        st.session_state['number_of_books'] = 5