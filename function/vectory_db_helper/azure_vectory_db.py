from function.AzureAIToken import *
# Import required libraries  
import os  
import json 
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.models import Vector  
from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    PrioritizedFields,  
    SemanticField,  
    SearchField,  
    SemanticSettings,  
    VectorSearch,  
    VectorSearchAlgorithmConfiguration,  
) 

from function.abstract_vectory_db.vectory_db import vectory_db
from function.openai_helper.openai_function import openai_helper

class azure_vectory_db(vectory_db):
    
    def __init__(self):  
        self.credential = AzureKeyCredential(AZURE_SEARCH_API_KEY)
        self.openai_helper = openai_helper()

    def create_index(self, index_name):
        # Create a search index
        index_client = SearchIndexClient(
            endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)

        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="product", type=SearchFieldDataType.String,filterable=True),
            SearchableField(name="category", type=SearchFieldDataType.String,filterable=True),

            SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=1536, vector_search_configuration="my-vector-config"),
        ]

        vector_search = VectorSearch(
            algorithm_configurations=[
                VectorSearchAlgorithmConfiguration(
                    name="my-vector-config",
                    kind="hnsw",
                    hnsw_parameters={
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 500,
                        "metric": "cosine"
                    }
                )
            ]
        )

        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=PrioritizedFields(
                title_field=SemanticField(field_name="product"),
                prioritized_keywords_fields=[SemanticField(field_name="category")],
                prioritized_content_fields=[SemanticField(field_name="content")]
            )
        )

        # Create the semantic settings with the configuration
        semantic_settings = SemanticSettings(configurations=[semantic_config])

        # Create the search index with the semantic settings
        index = SearchIndex(name=index_name, fields=fields,
                            vector_search=vector_search, semantic_settings=semantic_settings)
        result = index_client.create_or_update_index(index)
        return result

    def delete_index(self, index_name):
        # Delete a search index
        index_client = SearchIndexClient(
            endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)
        result = index_client.delete_index(index_name)
        return result

    def list_index_names(self):
        index_client = SearchIndexClient(endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, credential=self.credential)
        index_names = index_client.list_index_names()
        return index_names

    def upload_documents(self, index_name, documents):
        search_client = SearchClient(endpoint=AZURE_SEARCH_SERVICE_ENDPOINT, index_name=index_name, credential=self.credential)
        result = search_client.upload_documents(documents)
        return result
    
    def similarity_search(self, index_name, vector_fields, search_text):
        search_client = SearchClient(AZURE_SEARCH_SERVICE_ENDPOINT, index_name, credential=self.credential)  
        results = search_client.search(  
            search_text=None,  
            vector=self.openai_helper.get_embedding(search_text),
            top_k=5,
            vector_fields=vector_fields,
            select=["product", "category", "content"],
        )

        # for result in results:  
        #     print(f"cn: {result['cn']}")  
        #     print(f"en: {result['en']}")  
        #     print(f"Score: {result['@search.score']}")  
        #     print(f"updateby: {result['updateby']}")  
        #     print(f"customer: {result['customer']}")  
        #     print(f"Category: {result['category']}\n")  

        return results