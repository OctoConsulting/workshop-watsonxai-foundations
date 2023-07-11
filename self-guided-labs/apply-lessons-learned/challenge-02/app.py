import json
import os
import streamlit as st

from documentSearch import DocumentSearch
from os import listdir
from os.path import isfile, join

ROOT_DIR = "data"

# Detect all companies available to search
companies = []
for folder_name in listdir(ROOT_DIR):
        if not isfile(join(ROOT_DIR, folder_name)):
            companies.append(folder_name)
companies = sorted(companies)

questions = [   "How much debt does the company have and what are its yearly payments?",
                "How does the company reduce risk due to foreign current exposure?",
                "What litigation is pending and what monetary loss could occur?",
                "What acquisitions have completed and how much did they cost?"  ]

with st.sidebar:
    # Create drop down to select a company to search
    st.title('Search SEC 10K Filings')
    selected_company = st.selectbox('Select a company',
                                    companies, 
                                    key='company_selectbox')
    
    # Provide example questions
    st.divider()
    st.write('Example questions')
    button_clicks = []
    for i, question in enumerate(questions):
        button_clicks.append(st.button(question, key='button_' + str(i)))
    
    # Allow user to change how the app behaves
    st.divider()
    st.write('Options')
    is_passages_enabled = st.checkbox("Show model's response without passages to summarize")

    # Allow users to experiment with different model parameters
    with open("model_parameters.json", 'r') as json_file:
        default_model_parameters = json.load(json_file)
    model_parameters = st.text_area("Model Parameters", json.dumps(default_model_parameters))


# Restore cached questions if present
cached_question = ""
if "user_question_input" in st.session_state:
    cached_question = st.session_state.user_question_input    

# Use placeholder for UI element that we will configure later
placeholder = st.empty()

# Update input text when user selects an example question
question_text=cached_question
for i, button_click in enumerate(button_clicks):
    if button_click:
        question_text = questions[i]

# Buttons added so now place question field in our prior placeholder
user_question = placeholder.text_input("Enter your question", value=question_text, key='user_question_input')

# Add tabs for details about the models response
passage_count_to_summarize = 5
tab_answer, tab_top_passages, tab_prompt = st.tabs(["Summary", f"Top {passage_count_to_summarize} Passages", "Prompt"])

if user_question:
    # Load utilities to search the SEC 10Ks
    model_parameters_json = json.loads(model_parameters)
    sec_10k_search = DocumentSearch(model_parameters_json)

    # Load model response into tabs
    document_path = join(ROOT_DIR, selected_company)
    matching_passages = sec_10k_search.get_matching_passages(document_path, user_question, passage_count_to_summarize)
    prompt, summary = sec_10k_search.answer_question(document_path, selected_company, user_question, not is_passages_enabled, passage_count_to_summarize)
    with tab_answer:
        # Streamlit uses Latex which uses the dollar sign (4) as a special character so we must escape it as below.
        # https://discuss.streamlit.io/t/how-to-wrap-long-text-with-triggering-latex/33776
        summary = summary.replace("$", "\$")
        st.write(summary)

    with tab_top_passages:
        for passage in matching_passages:
            st.write(passage)

    with tab_prompt:
        st.write(prompt)

