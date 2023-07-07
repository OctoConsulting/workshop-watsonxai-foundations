import os

from chromadbSec10k import ChromaDBSEC10K

from dotenv import load_dotenv
from genai.model import Credentials
from genai.schemas import GenerateParams, ModelType 
from genai.extensions.langchain import LangChainInterface
from langchain.prompts import PromptTemplate
import streamlit as st

PASSAGE_PLACEHOLDER = "{passages}"

class SEC10KSearch:
    
    def __init__(self):
        self.load_model()
        self.chromaDb = ChromaDBSEC10K()

    def load_model(self):
        # Load credentials 
        load_dotenv(".env")
        api_key = os.getenv("GENAI_KEY", None)
        api_url = os.getenv("GENAI_API", None)
        creds = Credentials(api_key, api_url)

        # Create LLM
        params = GenerateParams(decoding_method="sample",
                                max_new_tokens=125,
                                min_new_tokens=10,
                                temperature=0.2,
                                #top_k=100,
                                #top_p=1, 
                                repetition_penalty=1)
        self.llm = LangChainInterface(model=ModelType.FLAN_UL2, params=params, credentials=creds)

    def get_all_passages_for_company(self, company_symbol):
        passages = []
        return passages

    def answer_question(self, company_symbol, company_name, question, is_use_rag, passage_count_to_summarize):

        if is_use_rag:
            question_prompt = f"Using these passages from the SEC 10K filed by {company_name}."
            question_prompt += f"\n\n {PASSAGE_PLACEHOLDER}" 
            question_prompt += f"\n\n Answer this question: {question}"
        else:
            question_prompt = f"Answer this question about {company_name}."
            question_prompt += f"\nquestion: {question}"

        matching_passages = self.get_matching_passages_for_company(company_symbol, question, passage_count_to_summarize)
        passages_str = ""
        for i, passage in enumerate(matching_passages):
            if i > 0:
                passages_str += "\n\n"
            passages_str += f"passage #{i+1}: {passage}"

        question_prompt = question_prompt.replace(PASSAGE_PLACEHOLDER, passages_str)
        summary = self.llm(question_prompt)
        return question_prompt, summary

    def get_matching_passages_for_company(self, company_symbol, question, passage_count_to_summarize):        
        matches = self.chromaDb.query(company_symbol, query_texts=[question], n_results=passage_count_to_summarize)
        return matches['documents'][0]


