# https://mcr.microsoft.com/en-us/product/devcontainers/base/about
# mcr.microsoft.com/devcontainers/base:ubuntu (latest LTS release)
# mcr.microsoft.com/devcontainers/base:ubuntu-22.04 (or jammy)
# mcr.microsoft.com/devcontainers/base:ubuntu-20.04 (or focal)
# mcr.microsoft.com/devcontainers/base:ubuntu-18.04 (or bionic)

FROM mcr.microsoft.com/devcontainers/base:ubuntu AS base

WORKDIR /app

RUN sudo apt-get update
RUN sudo apt-get install python3-pip -y

RUN apt-get update && apt-get install -y ffmpeg

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# RUN pip install azure-cli
# RUN pip install streamlit streamlit-authenticator streamlit-extras st-pages
# RUN pip install openai pandas openpyxl langchain tiktoken
# RUN pip install PyPDF2

# RUN pip install azure-identity
# RUN pip install azure-search-documents --pre

EXPOSE 80
COPY . .

ENTRYPOINT ["streamlit", "run", "page_home.py", "--server.port=8501", "--server.address=0.0.0.0"]