import random

import pandas as pd
import streamlit as st

from book_app import BookDisplay

if __name__ == '__main__':
    st.title("Recommendation App")
    
    data = pd.read_csv('./data/books.csv')

    # Add number_of_books variable into session_state if does not exist (first run)
    if 'number_of_books' not in st.session_state:
        st.session_state['number_of_books'] = 5

    # Add random_books variable into session_state if does not exist (first run)
    if 'random_books' not in st.session_state:
        st.session_state['random_books'] = random.randint(1, 1000)

    # Add a dictionary of rated books to keep track of the rated books.
    if 'rated_books' not in st.session_state:
        st.session_state['rated_books'] = {}

    #
    book_display = BookDisplay()

    search = st.text_input('Search a book by its title')

    f, s = st.columns(2)

    with f:
        if st.button('Load more books'):
            st.session_state['number_of_books'] += 5
    with s:
        if st.button('Show another sample of books'):
            st.session_state['random_books'] += 5
            st.session_state['number_of_books'] = 5  # SHOW ANOTHER SAMPLE IS NOT WORKING THE FIRST TIME

    # Generate books
    books_to_display, nb = BookDisplay.generate_books_to_rate(data, number_of_books=st.session_state['number_of_books'],
                                                              rstate=st.session_state['random_books'], search=search)

    # Display some useful information
    st.write(f'Number of books available : {nb}')
    st.write(f'Number of books displayed : {st.session_state["number_of_books"]}')
    st.write(f'__________')

    st.title(f'Books to rate')

    # Display the books
    book_display.display_books_to_rate(books_to_display, st.session_state['rated_books'])

    # BookDisplay.recommended_books(st.session_state['rated_books'])
    book_display.display_books_to_recommend(rated_books=st.session_state['rated_books'], number_of_recommended=10)
