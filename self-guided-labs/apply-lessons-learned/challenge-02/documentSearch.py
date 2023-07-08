import os

from chromadbWrapper import ChromaDBWrapper

from dotenv import load_dotenv
from genai.model import Credentials
from genai.schemas import GenerateParams, ModelType 
from genai.extensions.langchain import LangChainInterface
from langchain.prompts import PromptTemplate
import streamlit as st

PASSAGE_PLACEHOLDER = "{passages}"

class DocumentSearch:
    
    def __init__(self, model_parameters):
        self.load_model(model_parameters)
        self.chromaDb = ChromaDBWrapper()

    def load_model(self, model_parameters):
        # Load credentials 
        load_dotenv(".env")
        api_key = os.getenv("GENAI_KEY", None)
        api_url = os.getenv("GENAI_API", None)
        creds = Credentials(api_key, api_url)

        # Create LLM
        params = GenerateParams(decoding_method=model_parameters["decoding_method"],
                                max_new_tokens=model_parameters["max_new_tokens"],
                                min_new_tokens=model_parameters["min_new_tokens"],
                                temperature=model_parameters["temperature"],
                                top_k=model_parameters["top_k"],
                                top_p=model_parameters["top_p"], 
                                repetition_penalty=model_parameters["repetition_penalty"])
        self.llm = LangChainInterface(model=ModelType.FLAN_UL2, params=params, credentials=creds)

    def answer_question(self, document_path, company_name, question, is_use_rag, passage_count_to_summarize):

        if is_use_rag:
            question_prompt = f"Using these passages from the SEC 10K filed by {company_name}."
            question_prompt += f"\n\n {PASSAGE_PLACEHOLDER}" 
            question_prompt += f"\n\n Answer this question: {question}"
        else:
            question_prompt = f"Answer this question about {company_name}."
            question_prompt += f"\nquestion: {question}"

        matching_passages = self.get_matching_passages(document_path, question, passage_count_to_summarize)
        passages_str = ""
        for i, passage in enumerate(matching_passages):
            if i > 0:
                passages_str += "\n\n"
            passages_str += f"passage #{i+1}: {passage}"

        question_prompt = question_prompt.replace(PASSAGE_PLACEHOLDER, passages_str)
        summary = self.llm(question_prompt)
        return question_prompt, summary

    def get_matching_passages(self, document_path, question, passage_count_to_summarize):        
        matches = self.chromaDb.query(document_path, query_texts=[question], n_results=passage_count_to_summarize)
        passages = []
        for passage in matches['documents'][0]:
            # Streamlit uses Latex which uses the dollar sign (4) as a special character so we must escape it as below.
            # https://discuss.streamlit.io/t/how-to-wrap-long-text-with-triggering-latex/33776
            passage = passage.replace("$", "\$")
            passages.append(passage)
        return passages



