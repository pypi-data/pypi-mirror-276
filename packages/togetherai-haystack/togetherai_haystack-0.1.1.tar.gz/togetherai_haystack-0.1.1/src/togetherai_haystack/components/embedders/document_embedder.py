import itertools
from typing import Any, Dict, List, Optional, Tuple, TypedDict

from haystack import Document, component, default_from_dict, default_to_dict
from haystack.utils import Secret, deserialize_secrets_inplace
from together import Together
from tqdm import tqdm


@component
class TogetherAIDocumentEmbedder:
    """
    A component for computing Document embeddings using Together models.
    """

    class Meta(TypedDict):
        model: str

    def __init__(
        self,
        api_key: Secret = Secret.from_env_var("TOGETHER_API_KEY"),
        model: str = "togethercomputer/m2-bert-80M-2k-retrieval",
        api_base_url: Optional[str] = "https://api.together.xyz/v1",
        prefix: str = "",
        suffix: str = "",
        batch_size: int = 32,
        progress_bar: bool = True,
        meta_fields_to_embed: Optional[List[str]] = None,
        embedding_separator: str = "\n",
    ):
        """
        Create a TogetherDocumentEmbedder component.

        :param api_key:
            The Together API key.
        :param model:
            The name of the model to use.
        :param api_base_url:
            Overrides default base url for all HTTP requests.
        :param prefix:
            A string to add at the beginning of each text.
        :param suffix:
            A string to add at the end of each text.
        :param batch_size:
            Number of Documents to encode at once.
        :param progress_bar:
            If True shows a progress bar when running.
        :param meta_fields_to_embed:
            List of meta fields that will be embedded along with the Document text.
        :param embedding_separator:
            Separator used to concatenate the meta fields to the Document text.
        """
        self.api_key = api_key
        self.model = model
        self.api_base_url = api_base_url
        self.prefix = prefix
        self.suffix = suffix
        self.batch_size = batch_size
        self.progress_bar = progress_bar
        self.meta_fields_to_embed = meta_fields_to_embed or []
        self.embedding_separator = embedding_separator

        self.client = Together(
            api_key=api_key.resolve_value(),
            base_url=api_base_url,
        )

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
            prefix=self.prefix,
            suffix=self.suffix,
            batch_size=self.batch_size,
            progress_bar=self.progress_bar,
            meta_fields_to_embed=self.meta_fields_to_embed,
            embedding_separator=self.embedding_separator,
            api_key=self.api_key.to_dict(),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TogetherAIDocumentEmbedder":
        """
        Deserializes the component from a dictionary.

        :param data:
            Dictionary to deserialize from.
        :returns:
            Deserialized component.
        """
        deserialize_secrets_inplace(data["init_parameters"], keys=["api_key"])
        return default_from_dict(cls, data)

    def _document_text_to_embed(self, doc: Document) -> str:
        """
        Return the text to embed for a Document, by concatenating the Document text with the metadata fields to embed.
        """
        meta_values_to_embed = [
            str(meta_value)
            for (meta_key, meta_value) in doc.meta.items()
            if meta_key in self.meta_fields_to_embed and meta_value is not None
        ]

        return (
            self.prefix
            + self.embedding_separator.join(meta_values_to_embed + [doc.content or ""])
            + self.suffix
        )

    def _embed_batch(
        self, texts_to_embed: List[str], batch_size: int
    ) -> Tuple[List[List[float]], Meta]:
        """
        Embed a list of texts in batches.
        """

        all_embeddings = []
        meta: Dict[str, Any] = {}
        for batch in tqdm(
            itertools.batched(texts_to_embed, batch_size),
            disable=not self.progress_bar,
            desc="Calculating embeddings via Together.ai",
        ):
            response = self.client.embeddings.create(
                model=self.model, input=list(batch)
            )
            embeddings = [el.embedding for el in response.data]
            all_embeddings.extend(embeddings)

            if "model" not in meta:
                meta["model"] = response.model

        return all_embeddings, meta

    @component.output_types(documents=List[Document], meta=Meta)
    def run(self, documents: List[Document]):
        """
        Embed a list of Documents.

        :param documents:
            Documents to embed.

        :returns:
            A dictionary with the following keys:
            - `documents`: Documents with embeddings
            - `meta`: Information about the usage of the model.
        """
        if (
            not isinstance(documents, list)
            or documents
            and not isinstance(documents[0], Document)
        ):
            raise TypeError(
                "TogetherDocumentEmbedder expects a list of Documents as input."
                "In case you want to embed a string, please use the TogetherTextEmbedder."
            )

        texts_to_embed = [self._document_text_to_embed(doc) for doc in documents]

        embeddings, meta = self._embed_batch(
            texts_to_embed=texts_to_embed, batch_size=self.batch_size
        )

        for doc, emb in zip(documents, embeddings):
            doc.embedding = emb

        return {"documents": documents, "meta": meta}
