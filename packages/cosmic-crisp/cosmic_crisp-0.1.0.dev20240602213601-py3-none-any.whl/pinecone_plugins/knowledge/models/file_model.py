from pinecone_plugins.knowledge.data.core.client.model.inline_object1 import InlineObject1 as ChatRequest
from pinecone_plugins.knowledge.data.core.client.model.kb_file_model import KBFileModel as OpenAIFileModel
from pinecone_plugins.knowledge.data.core.client.model.knowledge_chat_knowledge_model_name_chat_completions_messages \
    import KnowledgeChatKnowledgeModelNameChatCompletionsMessages as ChatContext

from .chat import ChatResultModel

class FileModel:
    def __init__(self, file_model: OpenAIFileModel):
        self.file_model = file_model

        # initialize types so they can be accessed
        self.name = self.file_model.name
        self.created_on = self.file_model.created_on
        self.updated_on = self.file_model.updated_on
        self.metadata = self.file_model.metadata
        self.status = self.file_model.status
        self.mime_type = self.file_model.mime_type

    def __str__(self):
        return str(self.file_model)
    
    def __repr__(self):
        return repr(self.file_model)

    def __getattr__(self, attr):
        return getattr(self.file_model, attr) 
        chat_context = [ChatContext(role=ctx.role, content=ctx.content) for ctx in chat_context]

        context = ChatRequest(messages=chat_context)
        search_result = self.knowledge_data_api.chat_completion_knowledge_model(
            knowledge_model_name=self.name, 
            inline_object1=context
        )
        results = ChatResultModel(chat_result=search_result)
        return search_result 