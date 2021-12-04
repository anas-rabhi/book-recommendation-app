import streamlit as st
import numpy as np
import pandas as pd
from book_app import BookDisplay
data = pd.read_csv('./data/books.csv')

st.sidebar.write(
    "Recommanded movies")

books = BookDisplay.generate_books_to_rate(data, number_of_books= 5)

BookDisplay.display_books_to_rate(books)

