# import time
# import numpy as np
# import pandas as pd
# import streamlit as st

# _LOREM_IPSUM = """
# Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
# incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
# nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
# """

# def stream_data():
#     for word in _LOREM_IPSUM.split(" "):
#         yield word + " "
#         time.sleep(0.02)



#     st.expander("label", expanded=False)

#     for word in _LOREM_IPSUM.split(" "):
#         yield word + " "
#         time.sleep(0.02)


# if st.button("Stream data"):
#     st.write_stream(stream_data)


# # with st.expander("See explanation"):
# #     st.write(
# #         """
# #         This example demonstrates how to stream data to the frontend. The `st.write_stream`
# #         function can be used to write data to the frontend in a streaming fashion. This is
# #         useful when you want to display data as it becomes available, rather than waiting
# #         for all data to be available before displaying it.
# #         """
# #     )


import time  
import streamlit as st  
  
_LOREM_IPSUM = """  
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor  
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis  
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.  
"""  

def stream_data():  
    # 第一部分文本流式输出  
    for word in _LOREM_IPSUM.split(" "):  
        yield word + " "  
        time.sleep(0.02)  
      
    # 第二部分文本流式输出，位于展开器外部  
    for word in _LOREM_IPSUM.split(" "):  
        yield word + " "  
        time.sleep(0.02)  

with st.chat_message("assistant"):
    st.markdown("You are an AI assistant that helps people find information.")

if st.button("Stream data"):  
    with st.chat_message("assistant"):
        st.write_stream(stream_data)  
