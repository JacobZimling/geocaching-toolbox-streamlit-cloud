import streamlit as st


def toolbox_header(page_header: str):
    st.set_page_config(layout="wide", page_title="PihlZimling's geocaching toolbox")
    # st.set_page_config("PihlZimling's geocaching toolbox")
    st.title("PihlZimling's geocaching toolbox")
    if len(page_header.strip()) > 0:
        st.header(page_header)
    # st.write(''' <style>
    #
    #          /* code */
    #          button {
    #             background-color: red;
    #          }
    #
    #          </style>''', unsafe_allow_html=True)
    return
