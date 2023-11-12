import os

os.environ["OPENAI_API_KEY"] = ""

os.environ["AZURE_OPENAI_ENDPOINT"]= "https://.openai.azure.com"
os.environ["AZURE_OPENAI_API_KEY"]= ""
os.environ["AZURE_OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["CHAT_COMPLETION_MODEL"]= "gpt-4"
os.environ["EMBEDDING_MODEL"]="text-embedding-ada-002"

os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]="https://.search.windows.net"
os.environ["AZURE_SEARCH_API_KEY"]=""