import os
from enum import Enum
from openai import OpenAI
from openai import AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt  

class openai_type(Enum):
    openai = 1
    azure = 2

class openai_helper():

    def __init__(self, openai_type=openai_type.openai):
        if openai_type == openai_type.azure:
            # gets the API Key from environment variable AZURE_OPENAI_API_KEY
            AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
            self.client = AzureOpenAI(
                api_key=AZURE_OPENAI_API_KEY,
                # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
                api_version = os.environ.get('AZURE_OPENAI_API_VERSION'),
                # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
                azure_endpoint= os.environ.get("AZURE_OPENAI_ENDPOINT"),
            )
        else:
            # gets the API Key from environment variable OpenAI_API_KEY
            OpenAI_API_KEY = os.environ.get('OPENAI_API_KEY')
            self.client = OpenAI(api_key=OpenAI_API_KEY)
        pass

    def openAI_ChatCompletion(self, system_prompt, content, temperature=0):
        response = self.client.chat.completions.create(
            # model="gpt-4",
            model=os.environ.get("CHAT_COMPLETION_MODEL"),
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response.choices[0].message.content

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def generate_embeddings(self, text):
        try:
            # model="text-embedding-ada-002"
            model = os.environ.get("EMBEDDING_MODEL")
            # text = text.replace("\n", " ")
            return self.client.embeddings.create(input = [text], model=model).data[0].embedding
        except Exception as e:
            print(e)
            raise e