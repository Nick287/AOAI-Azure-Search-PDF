from abc import ABC, abstractmethod  
  
class vectory_db(ABC):  
    @abstractmethod  
    def create_index(self, index_name):  
        pass  

    @abstractmethod
    def delete_index(self, index_name):  
        pass

    @abstractmethod
    def list_index_names(self):  
        pass

    @abstractmethod
    def upload_documents(self, *args, **kwargs):  
        pass

    @abstractmethod
    def similarity_search(self):  
        pass


# class azure_vectory_db(vectory_db):  
#     def sound(self):  
#         return "Meow!"  
  
# class chroma_vectory_db(vectory_db):  
#     def sound(self):  
#         return "Woof!"  
  
# def make_sound(animal):  
#     print(animal.sound())  
