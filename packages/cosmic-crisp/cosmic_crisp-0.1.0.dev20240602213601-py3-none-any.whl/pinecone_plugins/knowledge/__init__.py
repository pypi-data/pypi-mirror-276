from pinecone_plugin_interface import PluginMetadata
from .knowledge import Knowledge


__installables__ = [
    PluginMetadata(
        target_object="Pinecone",
        namespace="knowledge",
        implementation_class=Knowledge
    ) 
]