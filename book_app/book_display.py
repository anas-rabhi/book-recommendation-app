import pandas as pd
import streamlit as st

import numpy as np
from typing import (Dict,
                    List,
                    Callable)

class BookDisplay:
    def generate_books_to_rate(data: pd.DataFrame, number_of_books: int = 20) -> pd.DataFrame:
        data = data.copy()
        #data.sort_values('average_rating')

        data = data[data.average_rating.astype(float) > 4]
        data = data.sample(n=number_of_books, random_state=44)
        data = data[['title', 'image_url', 'book_id']]
        data['Response'] = None

        return data

    def display_books_to_rate(data: pd.DataFrame):
        books = {}
        for rows in data.itertuples(index=False):
            with st.container():
                st.write(f'{rows.title}')
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
        st.write(books)

