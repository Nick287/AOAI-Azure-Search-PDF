from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from io import BytesIO
from langchain.text_splitter import MarkdownHeaderTextSplitter
import os


class document_intelligence:
    
    def get_page_content_list(self, bytes_data):
        DOCUMENTINTELLIGENCECLIENT_ENDPOINT = os.environ.get('DOCUMENTINTELLIGENCECLIENT_ENDPOINT')
        DOCUMENTINTELLIGENCECLIENT_KEY = os.environ.get('DOCUMENTINTELLIGENCECLIENT_KEY')

        document_intelligence_client = DocumentIntelligenceClient(endpoint=DOCUMENTINTELLIGENCECLIENT_ENDPOINT, credential=AzureKeyCredential(DOCUMENTINTELLIGENCECLIENT_KEY))

        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", 
            analyze_request=bytes_data, 
            content_type="application/octet-stream",
            # output_content_format="markdown"
        )
        result: AnalyzeResult = poller.result()

        page_content_list =[]

        for page in result.pages:
            # print(f"----Analyzing layout from page #{page.page_number}----")
            page_content = ""
            # print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")
            if page.lines:
                for line_idx, line in enumerate(page.lines):
                    page_content +=  line.content + "\n"
                    # words = get_words(page, line)
                    # print(
                    #     f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
                    # )
            page_content_list.append(page_content)

        return page_content_list

    def semantic_chuncking(self, bytes_data: BytesIO):
        """ Run semantic chuncking by MarkdownHeaderTextSplitter
        """
        DOCUMENTINTELLIGENCECLIENT_ENDPOINT = os.environ.get('DOCUMENTINTELLIGENCECLIENT_ENDPOINT')
        DOCUMENTINTELLIGENCECLIENT_KEY = os.environ.get('DOCUMENTINTELLIGENCECLIENT_KEY')

        document_intelligence_client = DocumentIntelligenceClient(endpoint=DOCUMENTINTELLIGENCECLIENT_ENDPOINT,
                                                                  credential=AzureKeyCredential(DOCUMENTINTELLIGENCECLIENT_KEY))

        poller = document_intelligence_client.begin_analyze_document(model_id="prebuilt-layout",
                                                                     analyze_request=bytes_data,
                                                                     content_type="application/octet-stream",
                                                                     output_content_format="markdown")
        result: AnalyzeResult = poller.result()

        # Split the document into chunks base on markdown headers.
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        splits = text_splitter.split_text(result["content"])

        return splits
