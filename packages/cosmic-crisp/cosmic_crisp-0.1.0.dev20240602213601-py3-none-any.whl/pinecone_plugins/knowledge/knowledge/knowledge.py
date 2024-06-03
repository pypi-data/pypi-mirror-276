import time
from typing import Optional, Dict, List

from pinecone_plugin_interface import PineconePlugin

from pinecone_plugins.knowledge.control.core.client.api.manage_knowledge_models_api import ManageKnowledgeModelsApi as ControlApiClient 
from pinecone_plugins.knowledge.control.core.client.model.inline_object import InlineObject as CreateModelRequest
from pinecone_plugins.knowledge.control.core.client import ApiClient

from pinecone_plugins.knowledge.models import KnowledgeModel

from pinecone.utils import setup_openapi_client

class Knowledge(PineconePlugin):
    """
    The `Knowledge` class configures and utilizes the Pinecone Knowledge Engine API to create and manage knowledge models.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required

    :param client_builder: A `pinecone.utils` closure of setup_openapi_client, configured and built in the Pinecone class.
    :type client_builder: `(type(OpenApiClient), type(ClientApiClass), str, **kwargs)->ClientApiClass`, required
    """
    def __init__(self, config, client_builder):
        self.config = config

        self.knowledge_control_api = client_builder(ApiClient, ControlApiClient, 'unstable', host="https://api-staging.pinecone.io")
        self.client_builder = client_builder

    def create_model(
        self, 
        knowledge_model_name: str, 
        metadata: dict[str, any] = {}, 
        timeout: Optional[int] = None,
    ) -> KnowledgeModel:
        """
        Creates a knowledge model with the specified name, metadata, and optional timeout settings.

        :param knowledge_model_name: The name to assign to the knowledge model.
        :type knowledge_model_name: str, required

        :param metadata: A dictionary containing metadata for the knowledge model.
        :type metadata: dict, optional

        :type timeout: int, optional
        :param timeout: Specify the number of seconds to wait until model operation is completed. If None, wait indefinitely; if >=0, time out after this many seconds;
            if -1, return immediately and do not wait. Default: None

        :return: KnowledgeModel object with properties `name`, `metadata`, 'status', 'updated_at' and `created_at`. 
        - The `name` property contains the name of the model. 
        - The `metadata` property contains the metadata provided. 
        - The `created_at` property contains the timestamp of when the model was created.
        - The `updated_at` property contains the timestamp of when the model was last updated. 
        - The `status` property contains the status of the model. This is one of:
            - 'Initializing' 
            - 'Ready'
            - 'Terminating'
            - 'Failed'

        Example:
        >>> metadata = {"author": "Jane Doe", "version": "1.0"}
        >>> model = (...).create_model(knowledge_model_name="example_model", metadata=metadata, timeout=30)
        >>> print(model)
         {'created_at': '2024-06-02T19:01:17Z',
          'metadata': {'author': 'Jane Doe', 'version': '1.0'},
          'name': 'example_model',
          'status': 'Ready',
          'updated_at': '2024-06-02T19:01:17Z'}
        """ 
        inline_object = CreateModelRequest(name=knowledge_model_name, metadata=metadata)
        knowledge_model = self.knowledge_control_api.create_knowledge_model(inline_object=inline_object)

        if timeout == -1:
            # still in processing state
            return KnowledgeModel(knowledge_model=knowledge_model, client_builder=self.client_builder)
        if timeout is None:
            while not knowledge_model.status == 'Ready':
                time.sleep(5)
                knowledge_model = self.describe_model(knowledge_model_name)
        else:
            while not knowledge_model.status == 'Ready' and timeout >= 0:
                time.sleep(5)
                timeout -= 5
                knowledge_model = self.describe_model(knowledge_model_name)

        if timeout and timeout < 0:
            raise (
                # TODO: clarify errors
                TimeoutError(
                    "Please call the describe_model API ({}) to confirm model status.".format(
                        "https://www.pinecone.io/docs/api/operation/knowledge/describe_model/"
                    )
                )
            )

        return KnowledgeModel(knowledge_model=knowledge_model, client_builder=self.client_builder)

    def describe_model(
        self, knowledge_model_name: str
    ) -> KnowledgeModel:
        """
        Describes a knowledge model with the specified name. Will raise a 404 if no model exists with the specified name.

        :param knowledge_model_name: The name to assign to the knowledge model.
        :type knowledge_model_name: str, required

        :return: KnowledgeModel object with properties `name`, `metadata`, 'status', 'updated_at' and `created_at`. 
        - The `name` property contains the name of the model. 
        - The `metadata` property contains the metadata provided. 
        - The `created_at` property contains the timestamp of when the model was created.
        - The `updated_at` property contains the timestamp of when the model was last updated. 
        - The `status` property contains the status of the model. This is one of:
            - 'Initializing' 
            - 'Ready'
            - 'Terminating'
            - 'Failed'

        Example:
        >>> model = (...).describe_model(knowledge_model_name="example_model")
        >>> print(model)
         {'created_at': '2024-06-02T19:01:17Z',
          'metadata': {'author': 'Jane Doe', 'version': '1.0'},
          'name': 'example_model',
          'status': 'Ready',
          'updated_at': '2024-06-02T19:01:17Z'}
        """ 
        
        knowledge_model = self.knowledge_control_api.get_knowledge_model(knowledge_model_name=knowledge_model_name)
        return KnowledgeModel(knowledge_model=knowledge_model, client_builder=self.client_builder)

    def list_models(
        self
    ) -> List[KnowledgeModel]:
        """
        Lists all knowledge models created from the current API Key. Will raise a 404 if no model exists with the specified name.

        :return: List of KnowledgeModel objects with properties `name`, `metadata`, 'status', 'updated_at' and `created_at`. 
        - The `name` property contains the name of the model. 
        - The `metadata` property contains the metadata provided. 
        - The `created_at` property contains the timestamp of when the model was created.
        - The `updated_at` property contains the timestamp of when the model was last updated. 
        - The `status` property contains the status of the model. This is one of:
            - 'Initializing' 
            - 'Ready'
            - 'Terminating'
            - 'Failed'

        Example:
        >>> models = (...).list_models(knowledge_model_name="example_model")
        >>> print(model)
         [{'created_at': '2024-06-02T19:01:17Z',
          'metadata': {'author': 'Jane Doe', 'version': '1.0'},
          'name': 'example_model',
          'status': 'Ready',
          'updated_at': '2024-06-02T19:01:17Z'}]
        """ 
        knowledge_models_resp = self.knowledge_control_api.list_knowledge_models()
        return [KnowledgeModel(knowledge_model=knowledge_model, client_builder=self.client_builder) for knowledge_model in knowledge_models_resp.knowledge_models]
    
    def delete_model(
        self, 
        knowledge_model_name: str,
        timeout: Optional[int] = None, 
    ) -> KnowledgeModel:
        """
        Deletes a knowledge model with the specified name. Will raise a 404 if no model exists with the specified name.

        :param knowledge_model_name: The name to assign to the knowledge model.
        :type knowledge_model_name: str, required

        :type timeout: int, optional
        :param timeout: Specify the number of seconds to wait until model operation is completed. If None, wait indefinitely; if >=0, time out after this many seconds;
            if -1, return immediately and do not wait. Default: None

        Example:
        >>> (...).delete_model(knowledge_model_name="example_model", timeout=-1)
        >>> (...).describe_model(knowledge_model_name="example_model")
         {'created_at': '2024-06-02T19:01:17Z',
          'metadata': {'author': 'Jane Doe', 'version': '1.0'},
          'name': 'example_model',
          'status': 'Terminating',
          'updated_at': '2024-06-02T19:01:17Z'}
        """ 
        
        self.knowledge_control_api.delete_knowledge_model(knowledge_model_name=knowledge_model_name)

        if timeout == -1:
            # still in processing state
            return
        if timeout is None:
            knowledge_model = self.describe_model(knowledge_model_name)
            while knowledge_model:
                time.sleep(5)
                try:
                    knowledge_model = self.describe_model(knowledge_model_name)
                except Exception:
                    knowledge_model = None
        else:
            knowledge_model = self.describe_model(knowledge_model_name)
            while knowledge_model and timeout >= 0:
                time.sleep(5)
                timeout -= 5
                try:
                    knowledge_model = self.describe_model(knowledge_model_name)
                except Exception:
                    knowledge_model = None

        if timeout and timeout < 0:
            raise (
                # TODO: clarify errors
                TimeoutError(
                    "Please call the describe_model API ({}) to confirm model status.".format(
                        "https://www.pinecone.io/docs/api/operation/knowledge/describe_model/"
                    )
                )
            ) 

    def Model(
        self, knowledge_model_name: str
    ) -> KnowledgeModel:
        """
        Describes a knowledge model with the specified name. Will raise a 404 if no model exists with the specified name.

        :param knowledge_model_name: The name to assign to the knowledge model.
        :type knowledge_model_name: str, required

        :return: KnowledgeModel object with properties `name`, `metadata`, 'status', 'updated_at' and `created_at`. 
        - The `name` property contains the name of the model. 
        - The `metadata` property contains the metadata provided. 
        - The `created_at` property contains the timestamp of when the model was created.
        - The `updated_at` property contains the timestamp of when the model was last updated. 
        - The `status` property contains the status of the model. This is one of:
            - 'Initializing' 
            - 'Ready'
            - 'Terminating'
            - 'Failed'

        Example:
        >>> model = (...).describe_model(knowledge_model_name="example_model")
        >>> print(model)
         {'created_at': '2024-06-02T19:01:17Z',
          'metadata': {'author': 'Jane Doe', 'version': '1.0'},
          'name': 'example_model',
          'status': 'Ready',
          'updated_at': '2024-06-02T19:01:17Z'}
        """
        return self.describe_model(knowledge_model_name)