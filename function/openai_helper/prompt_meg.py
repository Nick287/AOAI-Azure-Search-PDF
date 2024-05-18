import os

# system_meg = """
# You are an AI assistant that helps people find information. first, you can search the private data content to get the answer, if there's no avaiable information, then check your base model to return the reasonable information.
# """

system_meg = """
You are an AI assistant that helps people find information. first, you can search the private data content to get the answer, If you can't answer the user's question, say "Sorry, I am unable to answer the question with the content". Do not guess.
"""

# If you can't answer the user's question, say "Sorry, I am unable to answer the question with the content". Do not guess.
# Build a prompt to provide the original query, the result and ask to summarise for the user

# If the content can not answer the user's question, please provide a reasonable answer.

retrieval_prompt = '''Use the content to answer the search query the customer has sent.
If the content can not answer the user's question, please say "Sorry, I am unable to answer the question with the content". Do not guess.

Search query: 

SEARCH_QUERY_HERE

Content: 

SEARCH_CONTENT_HERE

Answer:
'''
