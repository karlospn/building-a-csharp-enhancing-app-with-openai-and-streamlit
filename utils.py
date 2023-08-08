import streamlit as st
import codecs

# Helper function for state and file management

def clear_state():
    for key in st.session_state.keys():
        del st.session_state[key]

def read_csharp_file(file):
    content = file.read()
    decoded_content = codecs.decode(content, 'utf-8')
    return decoded_content