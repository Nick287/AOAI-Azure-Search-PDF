FROM mcr.microsoft.com/devcontainers/base:ubuntu AS base

WORKDIR /app

RUN sudo apt-get update
RUN sudo apt-get install python3-pip -y

RUN pip install azure-cli
RUN pip install streamlit streamlit-authenticator streamlit-extras st-pages
RUN pip install openai pandas openpyxl langchain tiktoken
RUN pip install PyPDF2

RUN pip install azure-identity
RUN pip install azure-search-documents --pre

EXPOSE 80

COPY . .  

ENTRYPOINT ["streamlit", "run", "page_home.py", "--server.port=8501", "--server.address=0.0.0.0"]