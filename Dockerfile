FROM mcr.microsoft.com/devcontainers/base:ubuntu AS base

WORKDIR /app

RUN sudo apt-get update
RUN sudo apt-get install python3-pip -y

RUN pip install azure-cli
RUN pip install streamlit streamlit-authenticator streamlit-extras
RUN pip install openai pandas openpyxl langchain tiktoken
RUN pip install chromadb pypdf pycryptodome PyPDF2

# RUN pip install --index-url=https://pkgs.dev.azure.com/azure-sdk/public/_packaging/azure-sdk-for-python/pypi/simple/ azure-search-documents==11.4.0a20230509004
RUN pip install azure-identity
RUN pip install azure-search-documents --pre

EXPOSE 80

COPY . .  

# COPY userInfo/* /userInfo/  
# ENTRYPOINT ["streamlit", "run"]
# CMD ["home.py"]
# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]