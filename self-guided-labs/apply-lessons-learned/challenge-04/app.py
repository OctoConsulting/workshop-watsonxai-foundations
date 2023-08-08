import json

import streamlit as st
import pandas as pd

from documentSearch import DocumentSearch
from os import listdir
from os.path import isfile, join

ROOT_DIR = "data"
COMPANY_PLACEHOLDER = "{company_name}"
QUESTION_PLACEHOLDER = "{question}"

# Detect all companies available to search
companies = []
for folder_name in listdir(ROOT_DIR):
        if not isfile(join(ROOT_DIR, folder_name)):
            companies.append(folder_name)
companies = sorted(companies)

questions = [   "How much debt does the company have and what are its yearly payments?",
                "How does the company reduce risk due to foreign currency exposure?",
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
        button_clicks.append(st.button(question, key='examples_' + str(i)))
    
# Allow disabling rag to see what non-rag response looks like
is_rag_enabled = True
if "is_rag_disabled" in st.session_state:
    is_rag_enabled = not st.session_state.is_rag_disabled    

# How many passages to send to model for summarization
passage_count_to_summarize = 3
if "passage_count" in st.session_state:
    passage_count_to_summarize = int(st.session_state.passage_count)

# Load and populate prompt template
with open('prompt_template_rag.txt') as file:
    prompt_template_rag_original = file.read()
with open('prompt_template_no_rag.txt') as file:
    prompt_template_no_rag_original = file.read()

if is_rag_enabled:
    if "prompt_template_rag_custom" in st.session_state:
        prompt_template = st.session_state.prompt_template_rag_custom
    else:
        prompt_template = prompt_template_rag_original
else:
    if "prompt_template_no_rag_custom" in st.session_state:
        prompt_template = st.session_state.prompt_template_no_rag_custom
    else:
        prompt_template = prompt_template_no_rag_original

# Allow users to experiment with different model parameters
with open("model_parameters.json", 'r') as json_file:
    model_parameters_json = json.load(json_file)

if "custom_model_parameters" in st.session_state:
    model_parameters_json = json.loads(st.session_state.custom_model_parameters)

# Restore cached questions if present
cached_question = ""
if "user_question_input" in st.session_state:
    cached_question = st.session_state.user_question_input    

# Update input text when user selects an example question
question_text=cached_question
for i, button_click in enumerate(button_clicks):
    if button_click:
        question_text = questions[i]

# Buttons added so now place question field in our prior placeholder
user_question = st.text_input("Enter your question", value=question_text, key='user_question_input')

# Add tabs for details about the models response
tab_answer, tab_top_passages, tab_prompt, tab_settings = st.tabs(["Summary", f"Top {passage_count_to_summarize} Passages", "Prompt", "Settings"])

with tab_settings:
    if is_rag_enabled:
        st.text_area("Prompt Template (with RAG)", prompt_template_rag_original, key='prompt_template_rag_custom')
    else:
        st.text_area("Prompt Template (without RAG)", prompt_template_no_rag_original, key='prompt_template_no_rag_custom')
    st.text_area("Model Parameters", json.dumps(model_parameters_json), key='custom_model_parameters')
    st.text_input("Passage count to summarize", value=passage_count_to_summarize, key='passage_count')
    st.checkbox("Show model's response without passages to summarize", key='is_rag_disabled')

if not user_question:
    with tab_answer: st.write("Waiting for question...")
    with tab_top_passages: st.write("Waiting for question...")
    with tab_prompt: st.write("Waiting for question...")

else:
    # Update prompt template with current input
    prompt_template = prompt_template.replace(COMPANY_PLACEHOLDER, selected_company)
    prompt_template = prompt_template.replace(QUESTION_PLACEHOLDER, user_question)

    # Load model response into tabs
    sec_10k_search = DocumentSearch(model_parameters_json)
    document_path = join(ROOT_DIR, selected_company)
    # Find document with passages
    for file in listdir(document_path):
        if file.endswith("_passages.parquet"):
            parquet_passage_file = join(document_path, file)
            break

    matching_passages_original = sec_10k_search.get_matching_passages(parquet_passage_file, user_question, passage_count_to_summarize)
    matching_passages = []
    for passage in matching_passages_original:
        # Streamlit uses Latex which uses the dollar sign (4) as a special character so we must escape it as below.
        # https://discuss.streamlit.io/t/how-to-wrap-long-text-with-triggering-latex/33776
        matching_passages.append(passage.replace("$", "\$") )

    if not is_rag_enabled:
        passage_count_to_summarize = 0

    prompt_final, summary = sec_10k_search.answer_question(parquet_passage_file, user_question, prompt_template, passage_count_to_summarize)
    summary = summary.replace("$", "\$")
    prompt_final = prompt_final.replace("$", "\$")

    with tab_answer:
        st.write(summary)

    with tab_top_passages:
        if is_rag_enabled:
            for passage in matching_passages:
                st.write(passage)
        else:
            st.write("RAG disabled")

    with tab_prompt:
        st.write(prompt_final)
