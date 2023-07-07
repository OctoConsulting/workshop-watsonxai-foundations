import json
import os
import streamlit as st

from sec10kSearch import SEC10KSearch
from os import listdir
from os.path import isfile, join

ROOT_DIR = "data/sec_10k"
ticker_file = os.path.join(ROOT_DIR,"sec_company_symbols.json")
with open(ticker_file, 'r') as f:
    company_symbols_json = json.load(f)

# Detect all companies available to search
companies = []
symbol_lookup = {}
for folder_name in listdir(ROOT_DIR):
        if not isfile(join(ROOT_DIR, folder_name)):
            company_name = company_symbols_json[folder_name]
            company_str = company_name + " (" + folder_name + ")"
            companies.append(company_str)
            symbol_lookup[company_str] = folder_name

companies = sorted(companies)

# Create drop down to select a company to search
with st.sidebar:
    selected_company = st.selectbox('Select a company',
                                    companies, 
                                    key='company_selectbox')

# Load utilities to search the SEC 10Ks
sec_10k_search = SEC10KSearch()

# Restore cached questions if present
if "user_question_input" in st.session_state:
    cached_question = st.session_state.user_question_input
else:
    cached_question = ""

# Allow customer to enter a question to search    
st.header('Search SEC 10K Filings')
user_question = st.text_input("Enter your question about " + selected_company + " here", value=cached_question, key='user_question_input')

is_passages_enabled = st.checkbox("Exclude passages and show model's direct response")

passage_count_to_summarize = 3
tab_answer, tab_top_passages, tab_prompt = st.tabs(["Answer", f"Top {passage_count_to_summarize} Passages", "Prompt"])

if user_question:

    # Load tabs with responses
    company_symbol = symbol_lookup[selected_company]
    matching_passages = sec_10k_search.get_matching_passages_for_company(company_symbol, user_question, passage_count_to_summarize)
    prompt, summary = sec_10k_search.answer_question(company_symbol, selected_company, user_question, not is_passages_enabled, passage_count_to_summarize)
    with tab_answer:
        st.write(summary)

    with tab_top_passages:
        for passage in matching_passages:
            st.write(passage)

    #with tab_all_text:
    #    all_passages = sec_10k_search.get_all_passages_for_company(company_symbol)
    #    for passage in all_passages:
    #        st.write(passage)

    with tab_prompt:
        st.write(prompt)

