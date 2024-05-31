import os

import maitai._types as types
from maitai._evaluator import Evaluator as Evaluator
from maitai._inference import Inference as Inference
from maitai._openai import MaiTaiOpenAIClient as OpenAI

chat = OpenAI().chat


def initialize(api_key):
    from maitai._config import config
    config.initialize(api_key)


if os.environ.get("MAITAI_API_KEY") and os.environ.get("MAITAI_ENV") != "development":
    initialize(os.environ.get("MAITAI_API_KEY"))
