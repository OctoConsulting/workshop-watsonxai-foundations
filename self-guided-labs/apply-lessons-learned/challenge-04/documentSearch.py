import os

import streamlit as st

from chromadbWrapper import ChromaDBWrapper
from langChainInterface import LangChainInterface
from dotenv import load_dotenv

from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

PASSAGE_PLACEHOLDER = "{passages}"

class DocumentSearch:
    
    def __init__(self, model_parameters):
        self.load_model(model_parameters)
        self.current_parquet_passage_file = None
        
    def load_model(self, model_parameters):
        # Load credentials 
        load_dotenv()
        api_key = os.getenv("API_KEY", None)
        ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
        project_id = os.getenv("PROJECT_ID", None)
        if api_key is None or ibm_cloud_url is None or project_id is None:
            print("Ensure you copied the .env file that you created earlier into the same directory as this notebook")
        else:
            creds =  {
                "url": ibm_cloud_url,
                "apikey": api_key 
    }

        # Create LLM
        params = {
            GenParams.DECODING_METHOD: model_parameters["decoding_method"],
            GenParams.MIN_NEW_TOKENS: model_parameters["min_new_tokens"],
            GenParams.MAX_NEW_TOKENS: model_parameters["max_new_tokens"],
            GenParams.TEMPERATURE: model_parameters["temperature"],
            GenParams.TOP_K: model_parameters["top_k"],
            GenParams.TOP_P: model_parameters["top_p"],
            GenParams.RANDOM_SEED: model_parameters["random_seed"],
            GenParams.REPETITION_PENALTY: model_parameters["repetition_penalty"]
        }
        self.llm = LangChainInterface(model='google/flan-ul2', credentials=creds, params=params, project_id=project_id)


    def answer_question(self, parquet_passage_file, question, prompt_initial, passage_count_to_summarize):
        if passage_count_to_summarize > 0:
            passages = self.get_matching_passages(parquet_passage_file, question, passage_count_to_summarize)        
            passages_str = ""
            for i, passage in enumerate(passages):
                if i > 0:
                    passages_str += "\n\n"
                passages_str += f"passage #{i+1}: {passage}"
            prompt_final = prompt_initial.replace(PASSAGE_PLACEHOLDER, passages_str)
        else:
            prompt_final = prompt_initial
        summary = self.llm(prompt_final)
        return prompt_final, summary
    
    def get_matching_passages(self, parquet_passage_file, question, passage_count_to_summarize): 
        if self.current_parquet_passage_file is not parquet_passage_file:
            self.current_parquet_passage_file = parquet_passage_file
            self.chromaDb = ChromaDBWrapper(parquet_passage_file)
       
        matches = self.chromaDb.query(query_texts=[question], n_results=passage_count_to_summarize)
        passages = []
        for passage in matches['documents'][0]:
            passages.append(passage)
        return passages


