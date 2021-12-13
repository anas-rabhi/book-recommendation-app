import pandas as pd
import streamlit as st

import numpy as np
from typing import (Dict,
                    List,
                    Callable)


similarity_matrix = np.load('./data/similarity.npy')
all_books = pd.read_csv('./data/books.csv')

class BookDisplay:
    def __init__(self):
        self.var = 0

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
            number_of_books = data.shape[0]

        data = data.sample(n=number_of_books, random_state=rstate, replace=False)
        data = data[['book_id', 'title', 'image_url', 'book_id', 'average_rating']]
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
                    books[rows.book_id] = st.radio("Rate the movie", ('Not rated', 1, 2, 3, 4, 5), index=0, key={rows.book_id})

                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if books[rows.book_id] == 1: st.markdown("""<div style="text-align: center"> ⭐ </div>""",
                                                                        unsafe_allow_html=True)
                    if books[rows.book_id] == 2: st.markdown(
                        """<div style="text-align: center"> ⭐⭐ </div>""", unsafe_allow_html=True)
                    if books[rows.book_id] == 3: st.markdown(
                        """<div style="text-align: center"> ⭐⭐⭐ </div>""", unsafe_allow_html=True)
                    if books[rows.book_id] == 4: st.markdown(
                        """<div style="text-align: center"> ⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
                    if books[rows.book_id] == 5: st.markdown(
                        """<div style="text-align: center"> ⭐⭐⭐⭐⭐ </div>""", unsafe_allow_html=True)
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(pd.DataFrame(books, index=[0]))

    @staticmethod
    def display_books_to_recommend(rated_books: Dict, number_of_recommended: int):
        data = _recommend_books(rated_books, number_of_recommended)
        if data is None:
            return st.write('Rate some movies to get a recommendation. ')

        st.sidebar.title('Recommended Books')
        st.sidebar.write(f'_________________')

        for rows in data.itertuples(index=False):
            st.sidebar.write(f'{rows.original_title}, rating : {rows.average_rating}')
            st.sidebar.write(f'_________________')
            st.sidebar.image(rows.image_url)

            st.sidebar.write(f'_________________')



def _recommend_books(rated_books: Dict, number_of_recommended):  # not sure to keep it ?
    ###### IMPORTANT ######
    # not optimal, try to save a list of recommended books or return it and store it into streamlit session....
    recommended = pd.DataFrame()
    df = all_books[['book_id', 'original_title', 'image_url', 'average_rating']].copy()

    rated = rated_books
    rated = [(k, v) for k, v in rated.items() if v!='Not rated']
    rated = [(str(k), v) for k, v in rated if int(v) >= 3]

    if len(rated)==0:
        return df[df.average_rating>4].sample(n=number_of_recommended).reset_index(drop=True)

    for i in rated:
        recommended = recommended.append(_similarity(i[0], df))

    #return recommended.sample(n=max(len(rated),number_of_recommended)).reset_index(drop=True)
    return recommended.reset_index(drop=True)[:number_of_recommended]

def _similarity(book_id: str, data: pd.DataFrame):  # don't really need the data parameters-> find better way
    pred = data.copy()
    pred['book_id'] = pred['book_id'].astype(str)
    i = pred[pred['book_id'] == book_id].index[0]
    pred['similar'] = similarity_matrix[i]
    pred = pred[pred.book_id != book_id]
    pred = pred.sort_values(['similar'], ascending=False)

    return pred[:10]



