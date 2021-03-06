from typing import (Dict)

import numpy as np
import pandas as pd
import streamlit as st

similarity_matrix = np.load('./data/similarity.npy')
all_books = pd.read_csv('./data/books.csv')


class BookDisplay:
    @staticmethod
    def generate_books_to_rate(data: pd.DataFrame, number_of_books: int = 20, rstate: int = 44,
                               search: str = None) -> pd.DataFrame:
        """
        Generate a sample of books that would be rated by the user.
        """
        data = data.copy()
        data = data.drop_duplicates(subset=['title'])
        if str.lower(search) is not None:
            data = data[data.title.str.lower().str.contains(search)]
        # data.sort_values('average_rating')

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
        """
        Display the sample of books to rate.
        """

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
                    books[rows.book_id] = st.radio("Rate the movie", ('Not rated', 1, 2, 3, 4, 5), index=0,
                                                   key={rows.book_id})

                    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

                    if books[rows.book_id] == 1: st.markdown("""<div style="text-align: center"> ??? </div>""",
                                                             unsafe_allow_html=True)
                    if books[rows.book_id] == 2: st.markdown(
                        """<div style="text-align: center"> ?????? </div>""", unsafe_allow_html=True)
                    if books[rows.book_id] == 3: st.markdown(
                        """<div style="text-align: center"> ????????? </div>""", unsafe_allow_html=True)
                    if books[rows.book_id] == 4: st.markdown(
                        """<div style="text-align: center"> ???????????? </div>""", unsafe_allow_html=True)
                    if books[rows.book_id] == 5: st.markdown(
                        """<div style="text-align: center"> ??????????????? </div>""", unsafe_allow_html=True)
        st.write(' ')
        st.write(' ')
        st.write(' ')
        st.write(pd.DataFrame(books, index=[0]))

    def display_books_to_recommend(self, rated_books: Dict, number_of_recommended: int):
        """
        Display the recommended books.
        """
        data = self._recommend_books(rated_books=rated_books, number_of_recommended=number_of_recommended)
        if data is None:
            return st.write('Rate some movies to get a recommendation. ')

        st.sidebar.title('Recommended Books')
        st.sidebar.write(f'_________________')

        for rows in data.itertuples(index=False):
            st.sidebar.write(f'{rows.original_title}, rating : {rows.average_rating}')
            st.sidebar.write(f'_________________')
            st.sidebar.image(rows.image_url)

            st.sidebar.write(f'_________________')

    def _recommend_books(self, rated_books: Dict, number_of_recommended: int):
        # list_of_recommended: None):  # not sure to keep it ?
        """
        Generate the sample of recommended books.
        """
        ###### IMPORTANT ######
        # not optimal, try to save a list of recommended books or return it and store it into streamlit session....
        recommended = pd.DataFrame()
        # if list_of_recommended is not None:
        #    recommended = pd.DataFrame(list_of_recommended)

        df = all_books[['book_id', 'original_title', 'image_url', 'average_rating']].copy()

        rated = rated_books
        rated = [(k, v) for k, v in rated.items() if v != 'Not rated']
        rated = [(str(k), v) for k, v in rated if int(v) >= 3]

        if len(rated) == 0:
            return df[df.average_rating > 4].sample(n=number_of_recommended).reset_index(drop=True)

        for i in rated:
            recommended = recommended.append(self._similarity(i[0], df))

        recommended = recommended.reset_index(drop=True)
        # return recommended.sample(n=max(len(rated),number_of_recommended)).reset_index(drop=True)
        random_books = recommended.reset_index(drop=True)[int(number_of_recommended / 3):].sample(
            n=(number_of_recommended - int(number_of_recommended / 3)))

        return recommended.reset_index(drop=True)[:int(number_of_recommended / 3)].append(random_books).reset_index(
            drop=True)

    def _similarity(self, book_id: str, data: pd.DataFrame):  # don't really need the data parameters-> find better way
        """
        Find the 10th most similar books
        """
        pred = data.copy()
        pred['book_id'] = pred['book_id'].astype(str)
        i = pred[pred['book_id'] == book_id].index[0]
        pred['similar'] = similarity_matrix[i]
        pred = pred[pred.book_id != book_id]
        pred = pred.sort_values(['similar'], ascending=False)

        return pred[:10]
