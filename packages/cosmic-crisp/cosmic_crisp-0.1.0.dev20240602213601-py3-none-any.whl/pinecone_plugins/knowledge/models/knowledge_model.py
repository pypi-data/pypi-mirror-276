import os
import time
from typing import List, Optional

from pinecone_plugins.knowledge.data.core.client.api.manage_knowledge_models_api import ManageKnowledgeModelsApi as DataApiClient
from pinecone_plugins.knowledge.data.core.client.model.inline_object1 import InlineObject1 as ChatRequest
from pinecone_plugins.knowledge.data.core.client.model.kb_file_model import KBFileModel
from pinecone_plugins.knowledge.control.core.client.models import KnowledgeModel as OpenAIKnowledgeModel
from pinecone_plugins.knowledge.data.core.client.model.knowledge_chat_knowledge_model_name_chat_completions_messages \
    import KnowledgeChatKnowledgeModelNameChatCompletionsMessages as ChatContext
from pinecone_plugins.knowledge.data.core.client import ApiClient
from pinecone import config

from pinecone_plugins.knowledge.models.file_model import FileModel

from .chat import ChatResultModel, ChatContextModel

class KnowledgeModel:
    def __init__(self, knowledge_model: OpenAIKnowledgeModel, client_builder):
        self.knowledge_model = knowledge_model
        self.knowledge_data_api = client_builder(ApiClient, DataApiClient, 'unstable', host="staging-data.ke.pinecone.io")

        # initialize types so they can be accessed
        self.name = self.knowledge_model.name
        self.created_at = self.knowledge_model.created_at
        self.updated_at = self.knowledge_model.updated_at
        self.metadata = self.knowledge_model.metadata
        self.status = self.knowledge_model.status

    def __str__(self):
        return str(self.knowledge_model)
    
    def __repr__(self):
        return repr(self.knowledge_model)

    def __getattr__(self, attr):
        return getattr(self.knowledge_model, attr)
    
    def upload_file(
        self, 
        file_path: str,
        timeout: Optional[int] = None
    ) -> FileModel:
        """
        Uploads a file from the specified path to this knowledge model for internal processing.

        :param file_path: The path to the file that needs to be uploaded.
        :type file_path: str, required

        :type timeout: int, optional
        :param timeout: Specify the number of seconds to wait until file processing is done. If None, wait indefinitely; if >=0, time out after this many seconds;
            if -1, return immediately and do not wait. Default: None

        :return: FileModel object with the following properties:
            - id: The UUID of the uploaded file.
            - name: The name of the uploaded file.
            - created_on: The timestamp of when the file was created.
            - updated_on: The timestamp of the last update to the file.
            - metadata: Metadata associated with the file.
            - status: The status of the file.
            - mime_type: The MIME type of the file.

        Example:
        >>> km = (...).knowledge.Model("model_name")
        >>> file_model = km.upload_file(file_path="/path/to/file.txt") # use the default timeout
        >>> print(file_model)
          {'created_on': '2024-06-02T19:48:00Z',
          'id': '070513b3-022f-4966-b583-a9b12e0920ff',
          'metadata': None,
          'mime_type': 'txt'
          'name': 'tiny_file.txt',
          'status': 'Available',
          'updated_on': '2024-06-02T19:48:00Z'}
        """
        
        try:
            with open(file_path, 'rb') as file:
                upload_resp = self.knowledge_data_api.upload_file(knowledge_model_name=self.knowledge_model.name, file=file)

                # wait for status
                if timeout == -1:
                    # still in processing state
                    return FileModel(file_model=upload_resp)
                if timeout is None:
                    while not upload_resp.status == 'Available':
                        time.sleep(5)
                        upload_resp = self.describe_file(upload_resp.id)
                else:
                    while not upload_resp.status == 'Available' and timeout >= 0:
                        time.sleep(5)
                        timeout -= 5
                        upload_resp = self.describe_file(upload_resp.id)

                if timeout and timeout < 0:
                    raise (
                        # TODO: fix url
                        TimeoutError(
                            "Please call the describe_file API ({}) to confirm model status.".format(
                                "https://www.pinecone.io/docs/api/operation/knowledge/describe_model/"
                            )
                        )
                    )
                return FileModel(file_model=upload_resp)
        except FileNotFoundError:
            raise Exception(f"Error: The file at {file_path} was not found.")
        except IOError:
            raise Exception(f"Error: Could not read the file at {file_path}.")
    
    def describe_file(self, file_id: str) -> FileModel:
        """
        Describes a file with the specified file_id from this knowledge model. Includes information on its status and metadata.

        :param : The file id of the file to be described
        :type file_id: str, required

        :return: FileModel object with the following properties:
            - id: The UUID of the requested file.
            - name: The name of the requested file.
            - created_on: The timestamp of when the file was created.
            - updated_on: The timestamp of the last update to the file.
            - metadata: Metadata associated with the file.
            - status: The status of the file.
            - mime_type: The MIME type of the file.

        Example:
        >>> km = (...).knowledge.Model("model_name")
        >>> file_model = km.upload_file(file_path="/path/to/file.txt") # use the default timeout
        >>> print(file_model)
          {'created_on': '2024-06-02T19:48:00Z',
          'id': '070513b3-022f-4966-b583-a9b12e0290ff',
          'metadata': None,
          'mime_type': 'txt'
          'name': 'tiny_file.txt',
          'status': 'Available',
          'updated_on': '2024-06-02T19:48:00Z'}
        >>> km.describe_file(file_id='070513b3-022f-4966-b583-a9b12e0290ff')
          {'created_on': '2024-06-02T19:48:00Z',
          'id': '070513b3-022f-4966-b583-a9b12e0290ff',
          'metadata': None,
          'mime_type': 'txt'
          'name': 'tiny_file.txt',
          'status': 'Available',
          'updated_on': '2024-06-02T19:48:00Z'}
        """

        file = self.knowledge_data_api.describe_file(knowledge_model_name=self.name, kb_file_id=file_id)
        return FileModel(file_model=file) 

    def list_files(self) -> List[FileModel]:
        """
        Lists all uploaded files in this knowledge model.

        :return: List of FileModel objects with the following properties:
            - id: The UUID of the requested file.
            - name: The name of the requested file.
            - created_on: The timestamp of when the file was created.
            - updated_on: The timestamp of the last update to the file.
            - metadata: Metadata associated with the file.
            - status: The status of the file.
            - mime_type: The MIME type of the file.

        Example:
        >>> km = (...).knowledge.Model("model_name")
        >>> km.list_files()
          [{'created_on': '2024-06-02T19:48:00Z',
          'id': '070513b3-022f-4966-b583-a9b12e0290ff',
          'metadata': None,
          'mime_type': 'txt'
          'name': 'tiny_file.txt',
          'status': 'Available',
          'updated_on': '2024-06-02T19:48:00Z'}, ...]
        """
        files_resp = self.knowledge_data_api.list_files(self.name)
        return [FileModel(file_model=file) for file in files_resp.files]

    def delete_file(
        self, 
        file_id: str,
        timeout: Optional[int] = None 
    ):
        """
        Deletes a file with the specified file_id from this knowledge model.

        :param file_path: The path to the file that needs to be uploaded.
        :type file_path: str, required

        :type timeout: int, optional
        :param timeout: Specify the number of seconds to wait until file processing is done. If None, wait indefinitely; if >=0, time out after this many seconds;
            if -1, return immediately and do not wait. Default: None

        Example:
        >>> km = (...).knowledge.Model("model_name")
        >>> km.delete_file(file_id='070513b3-022f-4966-b583-a9b12e0290ff') # use the default timeout
        >>> km.list_files()
          []
        """
        self.knowledge_data_api.delete_file(knowledge_model_name=self.name, kb_file_id=file_id)

        if timeout == -1:
            # still in processing state
            return
        if timeout is None:
            file = self.describe_file(file_id=file_id)
            while file:
                time.sleep(5)
                try:
                    file = self.describe_file(file_id=file_id)
                except Exception:
                    file = None
        else:
            file = self.describe_file(file_id=file_id)
            while file and timeout >= 0:
                time.sleep(5)
                timeout -= 5
                try:
                    file = self.describe_file(file_id=file_id)
                except Exception:
                    file = None

        if timeout and timeout < 0:
            raise (
                TimeoutError(
                    "Please call the describe_model API ({}) to confirm model status.".format(
                        "https://www.pinecone.io/docs/api/operation/knowledge/describe_model/"
                    )
                )
            ) 

        
    def chat_completions(self, chat_context: List[ChatContextModel]) -> ChatResultModel:
        """
        Performs a chat completion request to the following knowledge model.

        :param chat_context: The current context for the chat request. The final element in the list represents the user query to be made from this context.
        :type chat_context: List[ChatContextModel] where ChatContextModel requires the following:
            ChatContextModel:
                - role: str, the role of the context ('user' or 'agent')
                - content: str, the content of the context
        
        :return: ChatResultModel with the following format:
            {
                "choices": [
                    {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
                        "role": "assistant"
                    },
                    "logprobs": null
                    }
                ],
                "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
                "model": "gpt-3.5-turbo-0613",
            }
        
        Example:
        >>> from pinecone_plugins.knowledge.models import ChatContextModel
        >>> km = (...).knowledge.Model("planets-km")
        >>> chat_context = [ChatContextModel(role='user', content='How old is the earth')]
        >>> resp = km.chat_completions(chat_context=chat_context)
        >>> print(resp)
        {'choices': [{'finish_reason': 'stop',
              'index': 0,
              'message': {'content': 'The age of the Earth is estimated to be '
                                     'about 4.54 billion years, based on '
                                     'evidence from radiometric age dating of '
                                     'meteorite material and Earth rocks, as '
                                     'well as lunar samples. This estimate has '
                                     'a margin of error of about 1%.',
                          'role': 'assistant'}}],
        'id': 'chatcmpl-9VmkSD9s7rfP28uScLlheookaSwcB',
        'model': 'planets-km'}
        """
        chat_context = [ChatContext(role=ctx.role, content=ctx.content) for ctx in chat_context]

        context = ChatRequest(messages=chat_context)
        search_result = self.knowledge_data_api.chat_completion_knowledge_model(
            knowledge_model_name=self.name, 
            inline_object1=context
        )
        results = ChatResultModel(chat_result=search_result)
        return search_result 