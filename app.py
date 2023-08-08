import streamlit as st
import openai
import os
from dotenv import load_dotenv
from llm import explain_code, suggest_code_improvements, generate_xml_comments, generate_unit_tests
from utils import read_csharp_file, clear_state

load_dotenv()

if os.getenv('AZURE_OPENAI_APIKEY') is None:
    st.error("AZURE_OPENAI_APIKEY not set. Please set this environment variable and restart the app.")
if os.getenv('AZURE_OPENAI_BASE_URI') is None:
    st.error("AZURE_OPENAI_BASE_URI not set. Please set this environment variable and restart the app.")
if os.getenv('AZURE_OPENAI_GPT4_MODEL_NAME') is None:
    st.error("AZURE_OPENAI_GPT4_MODEL_NAME not set. Please set this environment variable and restart the app.")

openai.api_type = "azure"
openai.api_base = os.getenv('AZURE_OPENAI_BASE_URI')
openai.api_version = "2023-05-15"
openai.api_key = os.getenv('AZURE_OPENAI_APIKEY')

st.title("CSharp GPT-4 file enhancer")

uploaded_file = st.file_uploader(label="Add a csharp file", type=["cs"], accept_multiple_files=False, on_change=clear_state)
if uploaded_file is not None:
    
    csharp_code = read_csharp_file(uploaded_file)
        
    with st.expander("Source code"):
        st.code(csharp_code, language='csharp')

    if st.button("Add XML comments"):
        with st.spinner("Generating XML comments..."):
            if 'xml_comments_csharp_code' in st.session_state.keys():
                with st.expander("Source code with XML comments"):
                    st.code(st.session_state['xml_comments_csharp_code'], language='csharp')   
            else:
                with st.expander("Source code with XML comments"):
                    xml_comments_csharp_code = generate_xml_comments(csharp_code)
                    xml_comments_csharp_code = xml_comments_csharp_code.strip("```").lstrip("csharp").strip()
                    st.code(xml_comments_csharp_code, language='csharp')          
                    st.session_state['xml_comments_csharp_code'] = xml_comments_csharp_code

    if st.button("Explain code"):
        with st.spinner("Explaining code..."):
            if 'csharp_code_explained' in st.session_state.keys():
                st.markdown(st.session_state['csharp_code_explained'])
            else:
                csharp_code_explained = explain_code(csharp_code)
                st.markdown(csharp_code_explained)
                st.session_state['csharp_code_explained'] = csharp_code_explained

    if st.button("Suggest code improvements"):
        with st.spinner("Searching for improvements..."):
            if 'csharp_code_improvements' in st.session_state.keys():
                st.markdown(st.session_state['csharp_code_improvements'])
            else:
                csharp_code_improvements = suggest_code_improvements(csharp_code)
                st.markdown(csharp_code_improvements)
                st.session_state['csharp_code_improvements'] = csharp_code_improvements

    if st.button("Generate unit tests"):
         with st.spinner("Trying to generate Unit Tests..."):
            if 'unit_tests_csharp_code' in st.session_state.keys():
                with st.expander("Unit Tests source code"):
                    st.code(st.session_state['unit_tests_csharp_code'], language='csharp')   
            else:
                with st.expander("Unit Tests source code"):
                    unit_tests_csharp_code = generate_unit_tests(csharp_code)
                    unit_tests_csharp_code = unit_tests_csharp_code.strip("```").lstrip("csharp").strip()
                    st.code(unit_tests_csharp_code, language='csharp')          
                    st.session_state['unit_tests_csharp_code'] = unit_tests_csharp_code
