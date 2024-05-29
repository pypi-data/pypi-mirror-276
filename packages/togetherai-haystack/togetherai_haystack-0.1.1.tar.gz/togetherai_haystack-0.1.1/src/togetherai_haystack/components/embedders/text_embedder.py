from typing import Any, Dict, List, Optional, TypedDict

from haystack import component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace
from together import Together


@component
class TogetherAITextEmbedder:
    """
    A component for embedding strings using TogetherAI models.

    Usage example:
    ```python
    from togetherai_haystack.components.embedders import TogetherAITextEmbedder

    text_to_embed = "I love pizza!"

    text_embedder = TogetherAITextEmbedder()

    print(text_embedder.run(text_to_embed))

    # {'embedding': [0.017020374536514282, -0.023255806416273117, ...],
    # 'meta': {'model': 'text-embedding-ada-002-v2',
    #          'usage': {'prompt_tokens': 4, 'total_tokens': 4}}}
    ```
    """

    class Meta(TypedDict):
        model: str

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var("TOGETHER_API_KEY"),
        model: str = "togethercomputer/m2-bert-80M-2k-retrieval",
        api_base_url: Optional[str] = None,
        prefix: str = "",
        suffix: str = "",
    ):
        """
        Create an TogetherAITextEmbedder component.

        :param api_key:
            The TogetherAI API key.
        :param model:
            The name of the model to use.
        :param api_base_url:
            Overrides default base url for all HTTP requests.
        :param prefix:
            A string to add at the beginning of each text.
        :param suffix:
            A string to add at the end of each text.
        """
        self.model = model
        self.api_base_url = api_base_url
        self.prefix = prefix
        self.suffix = suffix
        self.api_key = api_key

        self.client = Together(
            api_key=api_key.resolve_value(),
            base_url=api_base_url,
        )

    def _get_telemetry_data(self) -> Dict[str, Any]:
        """
        Data that is sent to Posthog for usage analytics.
        """
        return {"model": self.model}

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the component to a dictionary.

        :returns:
            Dictionary with serialized data.
        """
        return default_to_dict(
            self,
            model=self.model,
            api_base_url=self.api_base_url,
            organization=self.organization,
            prefix=self.prefix,
            suffix=self.suffix,
            dimensions=self.dimensions,
            api_key=self.api_key.to_dict(),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TogetherAITextEmbedder":
        """
        Deserializes the component from a dictionary.

        :param data:
            Dictionary to deserialize from.
        :returns:
            Deserialized component.
        """
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

    @component.output_types(embedding=List[float], meta=Meta)
    def run(self, text: str):
        """
        Embed a single string.

        :param text:
            Text to embed.

        :returns:
            A dictionary with the following keys:
            - `embedding`: The embedding of the input text.
            - `meta`: Information about the usage of the model.
        """
        if not isinstance(text, str):
            raise TypeError(
                "TogetherAITextEmbedder expects a string as an input."
                "In case you want to embed a list of Documents, please use the TogetherAIDocumentEmbedder."
            )

        text_to_embed = self.prefix + text + self.suffix
        response = self.client.embeddings.create(model=self.model, input=text_to_embed)
        meta = {"model": response.model}
        return {"embedding": response.data[0].embedding, "meta": meta}
