import chromadb
import os

import pandas as pd

from chromadb.api.types import EmbeddingFunction
from sentence_transformers import SentenceTransformer
from typing import Optional, Any, Iterable, List

class MiniLML6V2EmbeddingFunction(EmbeddingFunction):
    MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    def __call__(self, texts):
        return MiniLML6V2EmbeddingFunction.MODEL.encode(texts).tolist()

class ChromaDBWrapper:
    
    def __init__(self, document_path):
        self.load_documents(document_path)
    
    def load_documents(self, document_path):
        # Find document with passages
        
        for file in os.listdir(document_path):
            if file.endswith("_passages.parquet"):
                parquet_file = os.path.join(document_path, file)
                break
        
        self.sec_10k_df = pd.read_parquet(parquet_file)
        self.sec_10k_passsages = self.sec_10k_df["text"].values.tolist()
        self.sec_10k_passsage_ids = self.sec_10k_df["passage_id"].values.tolist()

        self._client_settings = chromadb.config.Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=document_path
        )
        self._client = chromadb.Client(self._client_settings)
        self._collection = self._client.get_or_create_collection(name = f"sec_10k_minilm6v2", 
                                                                 embedding_function = MiniLML6V2EmbeddingFunction())
        print("sec_10k_passsages: " +str(len(self.sec_10k_passsages)))

        self.initialize_db()

    def initialize_db(self):
        print(f"self._collection.count(): {self._collection.count()}")
        if self.is_empty():
            print("initializing db")
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
        self._collection.upsert(
            metadatas=metadata, documents=passsages, ids=ids
        )
        return ids

    def is_empty(self):
        return self._collection.count()==0

    def persist(self):
        self._client.persist()

    # return: the closest result to the given question
    def query(self, query_texts:str, n_results:int=5):
        return self._collection.query(query_texts=query_texts, n_results=n_results)