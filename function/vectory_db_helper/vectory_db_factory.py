from function.vectory_db_helper.azure_vectory_db import *
from function.vectory_db_helper.chroma_vectory_db import *

from enum import Enum

class vectory_db_factory(object):  
    def create_vectory_db(self, type):  
        if type == vectory_db_type.azure_cognitive_search:
            return azure_vectory_db()  
        elif type == vectory_db_type.chroma_db:
            return chroma_vectory_db()
        else:  
            raise ValueError("Invalid type.")
        

class vectory_db_type(Enum): 
    azure_cognitive_search = 1  
    chroma_db = 2 