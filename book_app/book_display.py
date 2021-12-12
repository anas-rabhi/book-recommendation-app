import pandas as pd
import streamlit as st

import numpy as np
from typing import (Dict,
                    List,
                    Callable)


similarity_matrix = np.load('../data/similarity.npy')
all_books = pd.read_csv('../data/books.csv')

class BookDisplay:
    def __init__(self):
        self._similarity(0)

    @staticmethod
    def generate_books_to_rate(data: pd.DataFrame,number_of_books: int = 20, rstate: int = 44, search: str = None) -> pd.DataFrame:
        data = data.copy()
        data = data.drop_duplicates(subset=['title'])
        if str.lower(search) is not None:
            data = data[data.title.str.lower().str.contains(search)]
        #data.sort_values('average_rating')

        data = data[data.ratings_count.astype(float) > 100000]

        nb_of_books = data.shape[0]

        if nb_of_books < number_of_books:
            print(data.shape[0])
            number_of_books = data.shape[0]

        data = data.sample(n=number_of_books, random_state=rstate, replace=False)
        data = data[['title', 'image_url', 'book_id', 'average_rating']]
        data['Response'] = None

        return data, nb_of_books

    @staticmethod
    def display_books_to_rate(data: pd.DataFrame, books: Dict):
        for rows in data.itertuples(index=False):
            with st.container():
                st.write(f'_________________')
                st.write(f'{rows.title}, rating : {rows.average_rating}')
                st.write(f'_________________')
                f, s = st.columns(2)

                with f:
                    st.image(rows.image_url)

                with s:
                    st.text(' ')
                    st.text(' ')
                    books[f'{rows.title}'] = st.radio("Rate the movie", ('Not rated', 1, 2, 3, 4, 5), index=0, key={rows.title})
                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if books[f'{rows.title}'] == 1: st.markdown("""<div style="text-align: center"> ⭐ </div>""",
                                                                        unsafe_allow_html=True)
                    if books[f'{rows.title}'] == 2: st.markdown(
                        """<div style="text-align: center"> ⭐⭐ </div>""", unsafe_allow_html=True)
                    if books[f'{rows.title}'] == 3: st.markdown(
                        """<div style="text-align: center"> ⭐⭐⭐ </div>""", unsafe_allow_html=True)
                    if books[f'{rows.title}'] == 4: st.markdown(
                        """<div style="text-align: center"> ⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
                    if books[f'{rows.title}'] == 5: st.markdown(
                        """<div style="text-align: center"> ⭐⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(pd.DataFrame(books, index=[0]))

    def refresh_bouton(self): # not sure to put it there
        return 0



    def _similarity_10(data: pd.DataFrame, book_id: str): # don't really need the data parameters-> find better way
        pred = all_books.copy()
        i = pred[pred['book_id'] == book_id].index[0]
        pred['similar'] = similarity_matrix[i]
        pred = pred[pred.book_id != book_id]
        pred = pred.sort_values(['similar'], ascending=False)

        return pred[:10]
