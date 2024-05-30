from pinecone_plugin_interface import PluginMetadata
from pinecone_plugins.knowledge.core.client import ApiClient
from pinecone_plugins.knowledge.core.client.api.manage_knowledge_bases_api import ManageKnowledgeBasesApi

from .knowledge import Knowledge

__installables__ = [
    PluginMetadata(
        target_object="Pinecone",
        namespace="knowledge",
        implementation_class=Knowledge,
        api_version="unstable",
        openapi_api_class=ManageKnowledgeBasesApi,
        openapi_api_client_class=ApiClient,
    )
]