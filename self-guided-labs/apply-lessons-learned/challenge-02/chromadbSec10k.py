import chromadb
import os
import uuid

import pandas as pd

from chromadb.api.types import EmbeddingFunction
from sentence_transformers import SentenceTransformer
from typing import Optional, Any, Iterable, List

class MiniLML6V2EmbeddingFunction(EmbeddingFunction):
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    def __call__(self, texts):
        return MiniLML6V2EmbeddingFunction.MODEL.encode(texts).tolist()

class ChromaDBSEC10K:
    
    def __init__(self):
        self.current_company = None

    def load_company_data(self, company_symbol):
        self.current_company = company_symbol
        self.data_dir = os.path.join("data", "sec_10k", company_symbol)
        file_name = company_symbol + "_2020_10K_Passages.parquet"
        file_path = os.path.join(self.data_dir, file_name)
        self.sec_10k_df = pd.read_parquet(file_path)
        self.sec_10k_passsages = self.sec_10k_df["text"].values.tolist()
        self.sec_10k_passsage_ids = self.sec_10k_df["passage_id"].values.tolist()

        self._client_settings = chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.data_dir
        )
        self._client = chromadb.Client(self._client_settings)
        self._collection = self._client.get_or_create_collection(name = f"sec_10k_minilm6v2", 
                                                                 embedding_function = MiniLML6V2EmbeddingFunction())
        self.initialize_db()

    def initialize_db(self):
        if self.is_empty():
            _ = self.upsert_texts(
                passsages = self.sec_10k_passsages,
                # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
                metadata=[{'passage': passage, 'id': id}
                        for (passage,id) in
                        zip(self.sec_10k_passsages, self.sec_10k_passsage_ids)],  # filter on these!
                ids=self.sec_10k_passsage_ids,  # unique for each doc
            )
            self.persist()

    def upsert_texts(
        self,
        passsages: Iterable[str],
        metadata: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectorstore.
        Args:
            :param texts (Iterable[str]): Texts to add to the vectorstore.
            :param metadatas (Optional[List[dict]], optional): Optional list of metadatas.
            :param ids (Optional[List[str]], optional): Optional list of IDs.
            :param metadata: Optional[List[dict]] - optional metadata (such as passage, etc.)
        Returns:
            List[str]: List of IDs of the added texts.
        """
        self._collection.upsert(
            metadatas=metadata, documents=passsages, ids=ids
        )
        return ids

    def is_empty(self):
        return self._collection.count()==0

    def persist(self):
        self._client.persist()

    # return: the closest result to the given question
    def query(self, company_symbol:str, query_texts:str, n_results:int=5):
        if self.current_company is not company_symbol:
            print("loading company: " + company_symbol)
            self.load_company_data(company_symbol)
        return self._collection.query(query_texts=query_texts, n_results=n_results)