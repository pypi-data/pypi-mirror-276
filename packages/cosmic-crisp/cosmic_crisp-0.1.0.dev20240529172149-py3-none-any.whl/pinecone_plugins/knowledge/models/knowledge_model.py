from typing import List
from pinecone_plugins.knowledge.core.client.api.manage_knowledge_bases_api import ManageKnowledgeBasesApi
from pinecone_plugins.knowledge.core.client.model.inline_object1 import InlineObject1
from pinecone_plugins.knowledge.core.client.model.inline_object2 import InlineObject2
from pinecone_plugins.knowledge.core.client.model.kb_file_model import KBFileModel
from pinecone_plugins.knowledge.core.client.models import KnowledgeBaseModel as OpenAIKnowledgeModel

from .search_context_model import SearchContextModel
from .search_result import SearchResult

class KnowledgeBase:
    def __init__(self, knowledge_base: OpenAIKnowledgeModel, api_client_builder):
        self.knowledge_base = knowledge_base
        self.knowledge_api = api_client_builder(ManageKnowledgeBasesApi)

    def __str__(self):
        return str(self.knowledge_model)
    
    def __repr__(self):
        return repr(self.knowledge_model)

    def __getattr__(self, attr):
        return getattr(self.knowledge_base, attr)

    def upload_file(self, path: str) -> KBFileModel:
        # this is a little weird
        try:
            with open(path, 'rb') as file:
                upload_resp = self.knowledge_api.upload_file(knowledge_base_name=self.knowledge_base.name, body=file)
                return upload_resp

        except FileNotFoundError:
            return f"Error: The file at {path} was not found."
        except IOError:
            return f"Error: Could not read the file at {path}."
    
    
    def describe_file(self, file_id: str) -> KBFileModel:
        file = self.knowledge_api.describe_file(file_id)
        return file

    def list_files(self) -> List[KBFileModel]:
        files_resp = self.knowledge_api.list_files(self.name)
        return files_resp.files

    def delete_file(self, file_id: str) -> bool:
        self.knowledge_api.delete_file(file_id)
        
    def search_completions(self, search_context: List[SearchContextModel]):
        context = InlineObject1(search_context=search_context)
        search_result = self.knowledge_api.search_completion_knowledge_base(
            knowledge_base_name=self.name, 
            search_context=context
        )
        results = SearchResult(search_result=search_result)
        return search_result 

    def search_context(self, search_context: List[SearchContextModel]):
        context = InlineObject2(search_context=search_context)
        search_result = self.knowledge_api.search_context_knowledge_base(
            knowledge_base_name=self.name, 
            search_context=context
        )
        results = SearchResult(search_result=search_result)
        return search_result 

