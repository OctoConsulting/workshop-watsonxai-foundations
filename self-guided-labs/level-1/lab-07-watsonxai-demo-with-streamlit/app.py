# Import environment loading library
from dotenv import load_dotenv
# Import IBMGen Library 
from genai.model import Credentials
from genai.schemas import GenerateParams, ModelType 
from genai.extensions.langchain import LangChainInterface
# Import langchain prompt templates
from langchain.prompts import PromptTemplate
# Import system libraries
import os
# Import streamlit for the UI 
import streamlit as st

# Load environment vars
load_dotenv(".env")

# Define credentials 
api_key = os.getenv("GENAI_KEY", None)
api_url = os.getenv("GENAI_API", None)
creds = Credentials(api_key, api_url)

# Define generation parameters 
params = GenerateParams(decoding_method="sample",
                        max_new_tokens=300,
                        min_new_tokens=30,
                        #stream=False,
                        temperature=0.2,
                        #top_k=100,
                        #top_p=1, 
                        repetition_penalty=1)

# Create an instance of the LLM
llm = LangChainInterface(model=ModelType.FLAN_UL2, params=params, credentials=creds)

# Title for the app
st.title('🤖 Building a Simple Front End')
# Prompt box 
prompt = st.text_input('Enter your prompt here')
# If a user hits enter
if prompt: 
    # Pass the prompt to the llm
    response = llm(prompt)
    # Write the output to the screen
    st.write(response)