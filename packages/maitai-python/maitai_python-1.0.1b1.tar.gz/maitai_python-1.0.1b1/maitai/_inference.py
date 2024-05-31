import time
from typing import Iterable

import aiohttp
import requests
from betterproto import Casing

from maitai._config import config
from maitai._maitai_client import MaiTaiClient
from maitai._types import ChunkQueue, EvaluateCallback, QueueIterable
from maitai_gen.chat import ChatCompletionParams, ChatCompletionRequest
from maitai_gen.inference import InferenceStreamResponse


class Inference(MaiTaiClient):

    def __init__(self):
        super().__init__()

    @classmethod
    def infer(cls, session_id, reference_id, action_type, application_ref_name, completion_params: ChatCompletionParams, evaluate_callback: EvaluateCallback = None,
              timeout=None) -> Iterable[InferenceStreamResponse]:
        apply_corrections = evaluate_callback is None
        chat_request: ChatCompletionRequest = cls.create_inference_request(application_ref_name, session_id, reference_id, action_type, apply_corrections, completion_params)
        if evaluate_callback:
            q = ChunkQueue()
            cls.run_async(cls.send_inference_request_async(chat_request, q, evaluate_callback))
            return QueueIterable(q, timeout=timeout)
        else:
            return cls.send_inference_request(chat_request)

    @classmethod
    def create_inference_request(cls, application_ref_name, session_id, reference_id, action_type, apply_corrections, completion_params: ChatCompletionParams):
        infer_request: ChatCompletionRequest = ChatCompletionRequest()
        infer_request.application_ref_name = application_ref_name
        infer_request.reference_id = reference_id
        infer_request.session_id = session_id
        infer_request.action_type = action_type
        infer_request.apply_corrections = apply_corrections
        infer_request.params = completion_params
        return infer_request

    @classmethod
    def send_inference_request(cls, chat_request: ChatCompletionRequest) -> Iterable[InferenceStreamResponse]:
        start = time.time()

        def consume_stream():
            host = config.maitai_host
            url = f'{host}/chat/completions/serialized'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': config.api_key
            }

            response = requests.post(url, headers=headers, data=chat_request.to_json(casing=Casing.SNAKE), verify=False, stream=True)
            if response.status_code != 200:
                print(f"Failed to send inference request. Status code: {response.status_code}. Error: {response.text}")
                return
            else:
                print(f"Successfully sent inference request. Status code: {response.status_code}")
            try:
                for line in response.iter_lines():
                    if line:
                        yield line
            finally:
                response.close()

        for resp in consume_stream():
            inference_response: InferenceStreamResponse = InferenceStreamResponse().from_json(resp)
            yield inference_response
        print(time.time() - start)

    @classmethod
    async def send_inference_request_async(cls, chat_request: ChatCompletionRequest, chunk_queue: ChunkQueue, evaluation_callback: EvaluateCallback):
        start = time.time()

        host = config.maitai_host
        url = f'{host}/chat/completions/serialized'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': config.api_key
        }
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(url, headers=headers, data=chat_request.to_json(casing=Casing.SNAKE)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    print(f"Failed to send evaluation request. Status code: {response.status}. Error: {error_text}")
                    chunk_queue.put("done")
                    return
                else:
                    print(f"Successfully sent evaluation request. Status code: {response.status}")
                last_item = None
                async for line in response.content:
                    if line:
                        inference_response: InferenceStreamResponse = InferenceStreamResponse().from_json(line)
                        chunk_queue.put(inference_response)
                        last_item = inference_response
                chunk_queue.put("done")
                if last_item is not None and last_item.evaluate_response:
                    evaluation_callback(last_item.evaluate_response)
        print(time.time() - start)
