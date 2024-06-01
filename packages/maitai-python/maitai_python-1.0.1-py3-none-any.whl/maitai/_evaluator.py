import json
from typing import Iterable

import aiohttp
import requests
from betterproto import Casing

from maitai._config import config
from maitai._maitai_client import MaiTaiClient
from maitai._types import EvaluateCallback
from maitai_gen.chat import ChatCompletionChunk, EvaluateRequest, EvaluateResponse, EvaluationContentType


def _get_content_type(content, partial=None):
    if partial is not None:
        return EvaluateResponse.PARTIAL_CONTENT
    if isinstance(content, str):
        return EvaluationContentType.TEXT
    elif isinstance(content, list):
        return EvaluationContentType.MESSAGE


class Evaluator(MaiTaiClient):

    def __init__(self):
        super().__init__()

    @classmethod
    async def evaluate_async(cls, session_id, reference_id, action_type, content, content_type=None, application_id=None, application_ref_name=None, callback=None):
        if content_type is None:
            content_type = _get_content_type(content)
        if content_type is None:
            raise Exception('Unable to automatically determine content_type')
        if application_id is None and application_ref_name is None:
            raise Exception('application_id or application_ref_name must be provided')
        eval_request: EvaluateRequest = cls.create_eval_request(application_id, application_ref_name, session_id, reference_id, action_type, content_type, content)
        if callback is None:
            return await cls.send_evaluation_request_async(eval_request)
        else:
            cls.run_async(cls.send_evaluation_request_async(eval_request, callback))
            return None

    @classmethod
    def evaluate(cls, session_id, reference_id, action_type, content, content_type=None, application_id=None, application_ref_name=None, callback=None, partial=None):
        if content_type is None:
            content_type = _get_content_type(content, partial)
        if content_type is None:
            raise Exception('Unable to automatically determine content_type')
        if application_id is None and application_ref_name is None:
            raise Exception('application_id or application_ref_name must be provided')
        eval_request: EvaluateRequest = cls.create_eval_request(application_id, application_ref_name, session_id, reference_id, action_type, content_type, content, partial=partial)
        if callback is None:
            return cls.send_evaluation_request(eval_request)
        else:
            cls.run_async(cls.send_evaluation_request_async(eval_request, callback))
            return None

    @classmethod
    def evaluate_realtime(cls, session_id, reference_id, action_type, content_type, content, application_ref_name, partial, fault_description, sentinel_id):
        eval_request: EvaluateRequest = cls.create_eval_request(None, application_ref_name, session_id, reference_id, action_type, content_type, content, partial=partial,
                                                                fault_description=fault_description)
        eval_request.sentinel_id = sentinel_id
        return cls.send_realtime_eval_request(eval_request)

    @classmethod
    def create_eval_request(cls, application_id, application_ref_name, session_id, reference_id, action_type,
                            content_type, content, partial=None, fault_description=None):
        eval_request: EvaluateRequest = EvaluateRequest()
        eval_request.evaluation_content_type = content_type
        if content_type == EvaluationContentType.TEXT:
            if type(content) != str:
                raise Exception('Content must be a string')
            eval_request.text_content = content
        elif content_type == EvaluationContentType.MESSAGE:
            eval_request.message_content = content
        elif content_type == EvaluationContentType.PARTIAL:
            eval_request.message_content = content
            eval_request.text_content = partial
        eval_request.application_id = application_id
        eval_request.application_ref_name = application_ref_name
        eval_request.session_id = session_id
        eval_request.reference_id = reference_id
        eval_request.action_type = action_type
        if fault_description:
            eval_request.fault_description = fault_description
        return eval_request

    @classmethod
    def update_session_context(cls, session_id, context, application_id=None, application_ref_name=None):
        if type(context) != dict:
            raise Exception('Context must be a dictionary')
        if application_id is None and application_ref_name is None:
            raise Exception('application_id or application_ref_name must be provided')
        session_context = {
            'application_id': application_id,
            'application_ref_name': application_ref_name,
            'session_id': session_id,
            'context': context
        }
        cls.run_async(cls.send_session_context_update(session_context))

    @classmethod
    def append_session_context(cls, session_id, context, application_id=None, application_ref_name=None):
        if type(context) != dict:
            raise Exception('Context must be a dictionary')
        if application_id is None and application_ref_name is None:
            raise Exception('application_id or application_ref_name must be provided')
        session_context = {
            'application_id': application_id,
            'application_ref_name': application_ref_name,
            'session_id': session_id,
            'context': context
        }
        cls.run_async(cls.send_session_context_append(session_context))

    @classmethod
    def update_application_context(cls, context, application_id=None, application_ref_name=None):
        if type(context) != dict:
            raise Exception('Context must be a dictionary')
        if application_id is None and application_ref_name is None:
            raise Exception('application_id or application_ref_name must be provided')
        application_context = {
            'application_id': application_id,
            'application_ref_name': application_ref_name,
            'context': context
        }
        cls.run_async(cls.send_application_context_update(application_context))

    @classmethod
    def append_application_context(cls, context, application_id=None, application_ref_name=None):
        if type(context) != dict:
            raise Exception('Context must be a dictionary')
        if application_id is None and application_ref_name is None:
            raise Exception('application_id or application_ref_name must be provided')
        application_context = {
            'application_id': application_id,
            'application_ref_name': application_ref_name,
            'context': context
        }
        cls.run_async(cls.send_application_context_append(application_context))

    @classmethod
    async def send_evaluation_request_async(cls, eval_request: EvaluateRequest, callback: EvaluateCallback = None):
        async def send_request():
            host = config.maitai_host
            url = f'{host}/evaluation/request'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': config.api_key
            }
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.post(url, headers=headers,
                                        data=eval_request.to_json(casing=Casing.SNAKE)) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"Failed to send evaluation request. Status code: {response.status}. Error: {error_text}")
                        return None
                    return await response.read()

        result = await send_request()
        if result is not None:
            eval_result = EvaluateResponse().from_json(result)
            if callback is not None:
                callback(eval_result)
            else:
                return eval_result

    @classmethod
    def send_evaluation_request(cls, eval_request: EvaluateRequest) -> EvaluateResponse:
        def send_request():
            host = config.maitai_host
            url = f'{host}/evaluation/request'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': config.api_key
            }
            # Use requests to send a synchronous POST request
            response = requests.post(url, headers=headers, data=eval_request.to_json(casing=Casing.SNAKE), verify=False)
            if response.status_code != 200:
                print(f"Failed to send evaluation request. Status code: {response.status_code}. Error: {response.text}")
                return None
            return response.content

        result = send_request()
        if result is not None:
            eval_result = EvaluateResponse().from_json(result)
            return eval_result

    @classmethod
    async def send_session_context_update(cls, session_context):
        async def send_context():
            try:
                host = config.maitai_host
                url = f'{host}/context/session'
                headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': config.api_key
                }
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.put(url, headers=headers, data=json.dumps(session_context)) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            print(
                                f"Failed to send session context update. Status code: {response.status}. Error: {error_text}")
                        else:
                            print(f"Successfully sent session context update. Status code: {response.status}")
            except Exception as e:
                print(f"An error occurred while sending session context update: {e}")

        await send_context()

    @classmethod
    async def send_session_context_append(cls, session_context):
        async def send_context():
            try:
                host = config.maitai_host
                url = f'{host}/context/session/append'
                headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': config.api_key
                }
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.put(url, headers=headers, data=json.dumps(session_context)) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            print(
                                f"Failed to send session context for append. Status code: {response.status}. Error: {error_text}")
                        else:
                            print(f"Successfully sent session context for append. Status code: {response.status}")
            except Exception as e:
                print(f"An error occurred while sending session context for append: {e}")

        await send_context()

    @classmethod
    async def send_application_context_update(cls, application_context):
        async def send_context():
            try:
                host = config.maitai_host
                url = f'{host}/context/application'
                headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': config.api_key
                }
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.put(url, headers=headers, data=json.dumps(application_context)) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            print(
                                f"Failed to send application context update. Status code: {response.status}. Error: {error_text}")
                        else:
                            print(f"Successfully sent application context update. Status code: {response.status}")
            except Exception as e:
                print(f"An error occurred while sending application context update: {e}")

        await send_context()

    @classmethod
    async def send_application_context_append(cls, application_context):
        async def send_context():
            try:
                host = config.maitai_host
                url = f'{host}/context/application/append'
                headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': config.api_key
                }
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.put(url, headers=headers, data=json.dumps(application_context)) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            print(
                                f"Failed to send application context for append. Status code: {response.status}. Error: {error_text}")
                        else:
                            print(f"Successfully sent application context for append. Status code: {response.status}")
            except Exception as e:
                print(f"An error occurred while sending application context for append: {e}")

        await send_context()

    @classmethod
    def send_realtime_eval_request(cls, eval_request: EvaluateRequest) -> Iterable[ChatCompletionChunk]:
        def consume_stream():
            host = config.maitai_host
            url = f'{host}/evaluation/realtime'
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': config.api_key
            }

            response = requests.post(url, headers=headers, data=eval_request.to_json(casing=Casing.SNAKE), verify=False, stream=True)
            if response.status_code != 200:
                print(f"Failed to send realtime evaluation request. Status code: {response.status_code}. Error: {response.text}")
                return
            try:
                for line in response.iter_lines():
                    if line:
                        yield line
            finally:
                response.close()

        for resp in consume_stream():
            inference_response: ChatCompletionChunk = ChatCompletionChunk().from_json(resp)
            yield inference_response
