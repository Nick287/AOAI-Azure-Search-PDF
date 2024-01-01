import streamlit as st
from st_pages import Page, show_pages, add_page_title

import os
import io
import openai
from pydub import AudioSegment  
from io import BytesIO 
from pydub.silence import detect_nonsilent  
import requests

WHISPER_TRANSCRIBE_WEB_API = os.environ.get('WHISPER_TRANSCRIBE_WEB_API')
WHISPER_TRANSCRIBE_API_KEY = os.environ.get('WHISPER_TRANSCRIBE_API_KEY')

def init():
    st.title('Azure Open AI Whisper')
    st.subheader('Whisper transcribe tool')

    formats = ["json", "text", "srt", "verbose_json", "vtt"]
    response_format = st.selectbox("Please select the script format.", formats, index=1)
    system_prompt = None
    
    if st.checkbox("Transcripts correction by GPT", value=False):
        system_prompt ="You are a helpful assistant for the company ZyntriQix. Your task is to correct any spelling discrepancies in the transcribed text. Make sure that ..."
        system_prompt = st.text_area("Please input prompt.", value=system_prompt, height=260)
    
    #mp3, mp4, mpeg, mpga, m4a, wav, and webm
    formats = ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']
    data_upload = st.file_uploader("Please Choose a AV(audio/video) file",type=formats)
    if data_upload is not None:
        # To read file as bytes:
        bytes_data = data_upload.getvalue()
        iofile = BytesIO(bytes_data) 

        with st.spinner(text="Analyzing file..."):
            audio_file = AudioSegment.from_file(iofile)
            
            byte_stream = io.BytesIO()  
            audio_file.export(byte_stream, format='mp3')  
            byte_stream.seek(0)  # reset pointer back to the start of the stream  
            byte_stream.name = "test.mp3"

            # Get the byte data from the BytesIO object  
            byte_data = byte_stream.getvalue()  
            # Calculate the size in MB  
            size_in_mb = len(byte_data) / (1024 * 1024)  
            # print(f"Size: {size_in_mb} MB") 

            # If size is greater than 24MB, split the data  
            max_size_in_bytes = int(24 * 1024 * 1024)
            if len(byte_data) > max_size_in_bytes:  
                chunks = [byte_data[i:i+max_size_in_bytes] for i in range(0, len(byte_data), max_size_in_bytes)]  
            else:  
                chunks = [byte_data] 

            st.info(f"Standardized audio files：{size_in_mb:.2f} MB")            
            
            transcripts = []  # List to store transcripts 

            # Loop over each chunk  
            for chunk in chunks:  
                # Convert bytes to BytesIO  
                chunk_stream = io.BytesIO(chunk)  
                chunk_stream.name = "test.mp3"
                
                formats = ["json", "text", "srt", "verbose_json", "vtt"]
                if response_format not in formats:
                    response_format = "vtt"

                payload = {'response_format': response_format}
                if system_prompt is not None:
                    st.info(f"system_prompt is {system_prompt} ")
                    payload['prompt'] = system_prompt

                files=[
                ('file',('test.mp3',chunk_stream ,'audio/mp3'))
                ]
                headers = {
                'api-key': WHISPER_TRANSCRIBE_API_KEY
                }

                response = requests.request("POST", WHISPER_TRANSCRIBE_WEB_API, headers=headers, data=payload, files=files)

                # Store the transcript  
                transcripts.append(response.text)  

            transcripts_text = "\n".join(transcripts)
            st.text_area("Transcripts", value=transcripts_text, height=300)
            pass

def main():
    init()

if __name__ == "__main__":
    main()