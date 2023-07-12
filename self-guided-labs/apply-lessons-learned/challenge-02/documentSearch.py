import math
import numpy as np
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
        self.current_parquet_passage_file = None
        
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

    def sum_of_summary_for_question(self, parquet_passage_file, question, prompt_initial, passage_count_to_summarize):
        # Summarize 2 passages at a time
        matching_passages = self.get_matching_passages(parquet_passage_file, question, passage_count_to_summarize)
        passages_to_summarize = np.array_split(matching_passages, math.ceil(passage_count_to_summarize/2))
        summaries = []
        for passages in passages_to_summarize:
            prompt_final, summary = self._summarize_passages(passages, prompt_initial)
            print(f"prompt_final: {prompt_final}")
            summaries.append(summary)
        return self._summarize_passages(summaries, prompt_initial)
    
    def answer_question(self, parquet_passage_file, question, prompt_initial, passage_count_to_summarize):
        passages = self.get_matching_passages(parquet_passage_file, question, passage_count_to_summarize)        
        return self._summarize_passages(passages, prompt_initial)
    
    def get_matching_passages(self, parquet_passage_file, question, passage_count_to_summarize): 
        if self.current_parquet_passage_file is not parquet_passage_file:
            self.current_parquet_passage_file = parquet_passage_file
            self.chromaDb = ChromaDBWrapper(parquet_passage_file)
       
        matches = self.chromaDb.query(query_texts=[question], n_results=passage_count_to_summarize)
        passages = []
        for passage in matches['documents'][0]:
            passages.append(passage)
        return passages

    # Private method
    def _summarize_passages(self, passages, prompt_initial):
        passages_str = ""
        for i, passage in enumerate(passages):
            if i > 0:
                passages_str += "\n\n"
            passages_str += f"passage #{i+1}: {passage}"
        prompt_final = prompt_initial.replace(PASSAGE_PLACEHOLDER, passages_str)
        summary = self.llm(prompt_final)
        return prompt_final, summary


