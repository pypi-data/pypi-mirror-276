import os

import maitai._types as types
from maitai._azure import MaiTaiAsyncAzureOpenAIClient as AsyncAzureOpenAI, MaitaiAzureOpenAIClient as AzureOpenAI
from maitai._evaluator import Evaluator as Evaluator
from maitai._inference import Inference as Inference
from maitai._openai import MaiTaiOpenAIClient as OpenAI
from maitai._openai_async import MaiTaiAsyncOpenAIClient as AsyncOpenAI

chat = OpenAI().chat


def initialize(api_key):
    from maitai._config import config
    config.initialize(api_key)


if os.environ.get("MAITAI_API_KEY") and os.environ.get("MAITAI_ENV") != "development":
    initialize(os.environ.get("MAITAI_API_KEY"))
