# Import required libraries  
import os  
import json  
import openai
from openai import AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt  
from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient, SearchIndexingBufferedSender  
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.models import (
    QueryAnswerType,
    QueryCaptionType,
    QueryCaptionResult,
    QueryAnswerResult,
    SemanticErrorMode,
    SemanticErrorReason,
    SemanticSearchResultsType,
    QueryType,
    VectorizedQuery,
    VectorQuery,
    VectorFilterMode,    
)
from azure.search.documents.indexes.models import (  
    ExhaustiveKnnAlgorithmConfiguration,
    ExhaustiveKnnParameters,
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    SemanticPrioritizedFields,
    SemanticField,  
    SearchField,  
    SemanticSearch,
    VectorSearch,  
    HnswAlgorithmConfiguration,
    HnswParameters,  
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    ExhaustiveKnnParameters,
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SearchIndex,  
    SemanticConfiguration,  
    SemanticField,  
    SearchField,  
    VectorSearch,  
    HnswParameters,  
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
)  

from function.abstract_vectory_db.vectory_db import vectory_db
from function.openai_helper.openai_function import *

import pandas as pd
import numpy as np  

class azure_vectory_db(vectory_db):
    
    def __init__(self):
        self.service_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
        self.credential = AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"])
        self.openai_helper = openai_helper()

    def create_index(self, index_name):
        # Create a search index
        index_client = SearchIndexClient(
            endpoint=self.service_endpoint, credential=self.credential)


        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
            SearchableField(name="content", type=SearchFieldDataType.String,filterable=True),
            SearchableField(name="product", type=SearchFieldDataType.String,filterable=True),
            SearchableField(name="category", type=SearchFieldDataType.String,filterable=True),
            SearchableField(name="page_num", type=SearchFieldDataType.String,filterable=True),
            SearchableField(name="file_name", type=SearchFieldDataType.String,filterable=True),
            SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                        searchable=True, vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile"),
        ]

        # Configure the vector search configuration  
        vector_search = VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name="myHnsw",
                    kind=VectorSearchAlgorithmKind.HNSW,
                    parameters=HnswParameters(
                        m=4,
                        ef_construction=400,
                        ef_search=500,
                        metric=VectorSearchAlgorithmMetric.COSINE
                    )
                ),
                ExhaustiveKnnAlgorithmConfiguration(
                    name="myExhaustiveKnn",
                    kind=VectorSearchAlgorithmKind.EXHAUSTIVE_KNN,
                    parameters=ExhaustiveKnnParameters(
                        metric=VectorSearchAlgorithmMetric.COSINE
                    )
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name="myHnswProfile",
                    algorithm_configuration_name="myHnsw",
                ),
                VectorSearchProfile(
                    name="myExhaustiveKnnProfile",
                    algorithm_configuration_name="myExhaustiveKnn",
                )
            ]
        )

        semantic_config = SemanticConfiguration(
            name="my-semantic-config",
            prioritized_fields=SemanticPrioritizedFields(
                title_field=SemanticField(field_name="product"),
                keywords_fields=[SemanticField(field_name="category")],
                content_fields=[SemanticField(field_name="content")]
            )
        )

        # Create the semantic settings with the configuration
        semantic_search = SemanticSearch(configurations=[semantic_config])

        # Create the search index with the semantic settings
        index = SearchIndex(name=index_name, fields=fields,
                            vector_search=vector_search, semantic_search=semantic_search)
        result = index_client.create_or_update_index(index)
        return result

    def delete_index(self, index_name):
        # Delete a search index
        index_client = SearchIndexClient(
            endpoint=self.service_endpoint, credential=self.credential)
        result = index_client.delete_index(index_name)
        return result

    def list_index_names(self):
        index_client = SearchIndexClient(endpoint=self.service_endpoint, credential=self.credential)
        index_names = index_client.list_index_names()
        return index_names

    def upload_documents(self, index_name, dataframe):

        _openai = openai_helper()
        dataframe = dataframe.rename(columns={'document': 'content'})  
        dataframe['product'] = dataframe["id"].apply(lambda x : "you can customise this field")
        dataframe['category'] = dataframe["id"].apply(lambda x : "you can customise this field")
        dataframe['contentVector'] = dataframe["content"].apply(lambda x : _openai.generate_embeddings(x))
        list_of_dict = dataframe.to_dict('records')  

        search_client = SearchClient(endpoint=self.service_endpoint, index_name=index_name, credential=self.credential)
        result = search_client.upload_documents(list_of_dict)
        return result
    
    def similarity_search(self, index_name, search_text):
        vector_fields = "contentVector"
        search_client = SearchClient(self.service_endpoint, index_name, credential=self.credential)

        vector_query = VectorizedQuery(
            vector=self.openai_helper.generate_embeddings(search_text), 
            k_nearest_neighbors=5, 
            fields=vector_fields)
        
        results = search_client.search(  
            search_text=None,  
            vector_queries= [vector_query],
            select=["product", "content", "category", "page_num", "file_name"],
        )  
        
        # for result in results:  
        #     print(f"Product: {result['product']}")  
        #     print(f"Score: {result['@search.score']}")  
        #     print(f"Content: {result['content']}")  
        #     print(f"Category: {result['category']}\n")  

        return results