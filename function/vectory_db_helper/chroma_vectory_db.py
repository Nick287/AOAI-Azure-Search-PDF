import chromadb
import os
import pandas as pd

from function.abstract_vectory_db.vectory_db import vectory_db

class chroma_vectory_db(vectory_db):    
    def __init__(self):
        current_path = os.getcwd()    
        self.data_path = current_path+"/chromedb/db"
        # current_path = "/mnt/azure"  
        # self.data_path = current_path + "/chromedb/db"  

    def delete_index(self, index_name):
        # Delete a search index
        client = chromadb.PersistentClient(path=self.data_path)
        result = client.delete_collection(index_name)
        return result
    
    def create_index(self, index_name):
        client = chromadb.PersistentClient(path=self.data_path)
        collection = client.get_or_create_collection(
        name=index_name,
        metadata={"hnsw:space": "cosine"} # l2 is the default
        )
        return collection
    
    def list_index_names(self):
        client = chromadb.PersistentClient(path=self.data_path)
        index_names = client.list_collections()
        collection_names = [collection.name for collection in client.list_collections()]  
        return collection_names
    
    def upload_documents(self, index_name, dataframe):

        documents = dataframe["document"].to_list()
        ids = dataframe["id"].to_list()  

        client = chromadb.PersistentClient(path=self.data_path)
        collection = client.get_collection(name=index_name)
        result = collection.add(
                                documents=documents,
                                # metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
                                ids=ids
                            )
        return result
    
    def similarity_search(self, index_name, search_text):
        client = chromadb.PersistentClient(path=self.data_path)
        collection = client.get_collection(name=index_name)
        results = collection.query(
            query_texts=[search_text],
            n_results=5,
            # where={"metadata_field": "is_equal_to_this"},
            # where_document={"$contains":"search_string"}
        )
    
        df_results = pd.DataFrame(results)
        return df_results