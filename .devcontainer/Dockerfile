FROM mcr.microsoft.com/devcontainers/base:ubuntu AS base

RUN sudo apt-get update
RUN sudo apt-get install python3-pip -y

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# RUN pip install azure-cli
# RUN pip install streamlit streamlit-authenticator streamlit-extras st-pages
# RUN pip install openai pandas openpyxl langchain tiktoken
# RUN pip install PyPDF2

# RUN pip install azure-identity
# RUN pip install azure-search-documents==11.4.0b6
