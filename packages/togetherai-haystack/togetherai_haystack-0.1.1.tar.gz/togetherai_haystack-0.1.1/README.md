# togetherai-haystack

`together-haystack` provides [Haystack](https://github.com/deepset-ai/haystack) components to use [Together.ai](www.together.ai) models in Haystack pipelines.

> [!CAUTION]
> This project is unofficial, and the authors are not affiliated with either Haystack or Together.AI

At the moment, the integration is limited to embedder components that use Together Embeddings Inference APIs.

* `TogetherAITextEmbedder` to embed strings / text
* `TogetherAIDocumentEmbedder` to embed a collection of Haystack documents.

Refer to Haystack's documentation to see how these can be plugged-in in Haystack Pipelines to build whatever you need to.

Support for Generators (LLM) and other resources offered by together will be added soon™.

## Usage

1. Install from pypi using your python dependency manager, e.g. `pip install togetherai-haystack`
2. Import and use as any haystack component:
   ```pycon
   >>> from togetherai_haystack.components.embedders import TogetherAITextEmbedder
   
   # by default the API KEY is read from the TOGETHER_API_KEY environment variable
   >>> text_embedder = TogetherTextEmbedder(model="togethercomputer/m2-bert-80M-32k-retrieval")
   >>> text_embedder.run("Together.ai provides optimized inference endpoints")
   {'embedding': [-0.3592394, 0.1824189, ...]}
   
   ```

## Development
This project uses [pdm](https://pdm-project.org) as a package manager and [ruff](https://github.com/astral-sh/ruff) as a formatter and linter.

The test suite is currently quite bad, there are just two "integration" tests which require a real API key and will invoke the real Together endpoints.
These means that:
* You need an account and to set up an API key to run these tests
* These tests require an internet connection and won't work if the environment can't reach https://api.together.xyz/v1 or if Together itself is nonresponsive.
* These tests will use your Together.ai account credit.
  Though, given their low prices and the minuscule number of tokens used in the tests, each run should cost you ~$0.0000008, meaning you'd have to run them ~12500 times before 1cent is taken from your account.