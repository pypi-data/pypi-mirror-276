import os
import unittest

from togetherai_haystack.components.embedders import TogetherAIDocumentEmbedder
from haystack import Document


class TogetherDocumentEmbedderTestCase(unittest.TestCase):
    @unittest.skipIf(
        not os.environ.get("TOGETHER_API_KEY", None),
        "Set the TOGETHER_API_KEY if you want to run this integration test.",
    )
    def test_compute_embeddings(self):
        docs = [
            Document(
                content="Together.ai is the fastest cloud platform for running generative AI."
            ),
            Document(
                content="Inference that’s fast, simple, and scales as you grow.",
                meta={"topic": "AI"},
            ),
        ]
        embedder = TogetherAIDocumentEmbedder()
        result = embedder.run(docs)
        self.assertIn("documents", result)
        for doc in result["documents"]:
            self.assertIsInstance(doc.embedding, list)
            self.assertIsInstance(doc.embedding[0], float)

        self.assertIn("meta", result)
        self.assertIn("model", result["meta"])
        self.assertIsInstance(result["meta"]["model"], str)
