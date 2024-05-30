from typing import Optional, Dict, List

from pinecone_plugin_interface import PineconePlugin

from pinecone_plugins.knowledge.core.client.api.manage_knowledge_bases_api import ManageKnowledgeBasesApi
from pinecone_plugins.knowledge.core.client.model.inline_object import InlineObject

from pinecone_plugins.knowledge.models import KnowledgeBase

class Knowledge(PineconePlugin):
    """
    The `Knowledge` class configures and utilizes the Pinecone Inference API to generate embeddings.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required
    """

    def __init__(self, config, knowledge_api):
        self.config = config
        self.knowledge_api = knowledge_api

    # methods I might need?
    # not sure if metadata will work
    def create_base(
        self, knowledge_base_name: str, metadata: dict[str, any]
    ) -> KnowledgeBase:
        inline_objects = InlineObject(name=knowledge_base_name, metadata=metadata)
        knowledge_base = self.knowledge_api.create_knowledge_base(inline_objects=inline_objects)

        return KnowledgeBase(knowledge_base=knowledge_base)

    def describe_base(
        self, knowledge_base_name: str
    ) -> KnowledgeBase:
        knowledge_base = self.knowledge_api.get_knowledge_base(name=knowledge_base_name)
        return KnowledgeBase(knowledge_base=knowledge_base)

    def list_bases(
        self, knowledge_base_name: str
    ) -> List[KnowledgeBase]:
        knowledge_bases_resp = self.knowledge_api.list_knowledge_bases()
        return [KnowledgeBase(knowledge_base=knowledge_base) for knowledge_base in knowledge_bases_resp.knowledge_bases]
    

    def Base(
        self, knowledge_base_name: str
    ) -> KnowledgeBase:
        return self.describe_base(knowledge_base_name)