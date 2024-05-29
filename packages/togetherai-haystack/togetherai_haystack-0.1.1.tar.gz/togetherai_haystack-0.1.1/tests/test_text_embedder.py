import os
import unittest

from togetherai_haystack.components.embedders import TogetherAITextEmbedder


class TogetherTextEmbedderTestCase(unittest.TestCase):
    @unittest.skipIf(
        not os.environ.get("TOGETHER_API_KEY", None),
        "Set the TOGETHER_API_KEY if you want to run this integration test.",
    )
    def test_compute_embeddings(self):
        embedder = TogetherAITextEmbedder()
        result = embedder.run("What is together.ai?")
        self.assertIn("embedding", result)
        self.assertIsInstance(result["embedding"], list)
        self.assertIsInstance(result["embedding"][0], float)
        self.assertIn("meta", result)
        self.assertIn("model", result["meta"])
        self.assertIsInstance(result["meta"]["model"], str)
