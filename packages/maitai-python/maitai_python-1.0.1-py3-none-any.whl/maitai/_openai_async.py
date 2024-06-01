from typing import AsyncIterable, Dict, Iterable, List, Mapping, Optional, Union

import httpx
import openai
import openai.types as openai_types
import openai.types.chat as openai_chat_types

import maitai
from maitai._config import config
from maitai._openai_types import Body, Headers, Query
from maitai._types import EvaluateCallback
from maitai._utils import convert_open_ai_chat_completion_chunk, convert_openai_chat_completion, get_chat_completion_params, process_chunk, process_stream_response, required_args, \
    set_completion_evaluation_response
from maitai_common.processes.stream_evaluation_thread import StreamEvaluationThread
from maitai_common.utils.proto_utils import openai_messages_to_proto
from maitai_gen.chat import ChatCompletionChunk, ChatCompletionResponse, ChatMessage, EvaluateResponse, EvaluationContentType
from maitai_gen.inference import InferenceStreamResponse

DEFAULT_MAX_RETRIES = 2


class MaiTaiAsyncOpenAIClient:
    def __init__(
        self,
        *,
        maitai_api_key: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        project: Optional[str] = None,
        base_url: Union[str, httpx.URL, None] = None,
        timeout: Union[float, httpx.Timeout, None, openai.NotGiven] = openai.NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        http_client: Optional[httpx.Client] = None,
        _strict_response_validation: bool = False,

    ):
        if maitai_api_key:
            config.initialize(maitai_api_key)
        self.client = openai.AsyncClient(
            api_key=api_key,
            organization=organization,
            project=project,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
        )

        self.chat = AsyncChat(self.client)


class AsyncChat:
    def __init__(self, client=None):
        self.completions = AsyncCompletions(client)


class AsyncCompletions:
    def __init__(self, client: Optional[openai.AsyncClient] = None):
        if client is None:
            client = openai.AsyncClient()
        self.client = client

    @required_args(["session_id", "action_type", "application_ref_name", "messages", "model"],
                   ["session_id", "action_type", "application_ref_name", "messages", "model", "stream"])
    async def create(
        self,
        *,
        # Maitai Arguments
        session_id: Union[str, int] = None,
        reference_id: Union[str, int, None] = None,
        action_type: str = None,
        application_ref_name: str = None,
        callback: Optional[EvaluateCallback] = None,
        server_side_inference: bool = False,  # TODO make this a config item
        # OpenAI Arguments
        messages: Iterable[openai_chat_types.ChatCompletionMessageParam],
        model: Union[str, openai_types.ChatModel],
        frequency_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        function_call: Union[openai_chat_types.completion_create_params.FunctionCall, openai.NotGiven] = openai.NOT_GIVEN,
        functions: Union[Iterable[openai_chat_types.completion_create_params.Function], openai.NotGiven] = openai.NOT_GIVEN,
        logit_bias: Union[Optional[Dict[str, int]], openai.NotGiven] = openai.NOT_GIVEN,
        logprobs: Union[Optional[bool], openai.NotGiven] = openai.NOT_GIVEN,
        max_tokens: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        n: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        presence_penalty: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        response_format: Union[openai_chat_types.completion_create_params.ResponseFormat, openai.NotGiven] = openai.NOT_GIVEN,
        seed: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        stop: Union[Union[Optional[str], List[str]], openai.NotGiven] = openai.NOT_GIVEN,
        stream: Optional[bool] = False,
        stream_options: Union[Optional[openai_chat_types.ChatCompletionStreamOptionsParam], openai.NotGiven] = openai.NOT_GIVEN,
        temperature: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        tool_choice: Union[openai_chat_types.ChatCompletionToolChoiceOptionParam, openai.NotGiven] = openai.NOT_GIVEN,
        tools: Union[Iterable[openai_chat_types.ChatCompletionToolParam], openai.NotGiven] = openai.NOT_GIVEN,
        top_logprobs: Union[Optional[int], openai.NotGiven] = openai.NOT_GIVEN,
        top_p: Union[Optional[float], openai.NotGiven] = openai.NOT_GIVEN,
        user: Union[str, openai.NotGiven] = openai.NOT_GIVEN,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, None, openai.NotGiven] = openai.NOT_GIVEN,
    ) -> Union[ChatCompletionResponse, AsyncIterable[ChatCompletionChunk]]:
        if not config.api_key:
            raise ValueError("Maitai API Key has not been set")
        if server_side_inference:
            completion_params = get_chat_completion_params(
                messages=messages,
                model=model,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                logprobs=logprobs,
                max_tokens=max_tokens,
                n=n,
                presence_penalty=presence_penalty,
                response_format=response_format,
                seed=seed,
                stop=stop,
                stream=stream,
                stream_options=stream_options,
                temperature=temperature,
                tool_choice=tool_choice,
                tools=tools,
                top_logprobs=top_logprobs,
                top_p=top_p,
                user=user,
            )
            response_timeout = None
            if isinstance(timeout, float) or isinstance(timeout, int):
                response_timeout = timeout
            response = await maitai.Inference.infer_async(session_id, reference_id, action_type, application_ref_name, completion_params, callback, timeout=response_timeout)
            if stream:
                return _process_inference_stream_async(response, callback)
            # ChatCompletion only
            chat_completion: Optional[ChatCompletionResponse] = None
            async for resp in response:
                if callback:
                    return resp.chat_completion_response
                else:
                    if resp.chat_completion_response:
                        chat_completion = resp.chat_completion_response
                    if resp.evaluate_response and chat_completion:
                        set_completion_evaluation_response(chat_completion, resp.evaluate_response)
                        return chat_completion
            return chat_completion
        else:
            response = await self.client.chat.completions.create(
                messages=messages,
                model=model,
                frequency_penalty=frequency_penalty,
                function_call=function_call,
                functions=functions,
                logit_bias=logit_bias,
                logprobs=logprobs,
                max_tokens=max_tokens,
                n=n,
                presence_penalty=presence_penalty,
                response_format=response_format,
                seed=seed,
                stop=stop,
                stream=stream,
                stream_options=stream_options,
                temperature=temperature,
                tool_choice=tool_choice,
                tools=tools,
                top_logprobs=top_logprobs,
                top_p=top_p,
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,

            )
            if stream:
                return _process_async_openai_stream(session_id, reference_id, action_type, application_ref_name, messages, response, callback)
            else:
                maitai_completion = convert_openai_chat_completion(response)
                proto_messages = openai_messages_to_proto(messages)
                proto_messages.append(
                    ChatMessage(role="assistant", content=maitai_completion.choices[0].message.content))
                maitai_eval = await maitai.Evaluator.evaluate_async(
                    session_id=session_id,
                    reference_id=reference_id,
                    action_type=action_type,
                    content_type=EvaluationContentType.MESSAGE,
                    content=proto_messages,
                    application_ref_name=application_ref_name,
                    callback=callback,
                )
                if not callback:
                    set_completion_evaluation_response(maitai_completion, maitai_eval)
                return maitai_completion


async def _process_async_openai_stream(session_id: Union[str, int],
                                       reference_id: Union[str, int, None],
                                       action_type: str,
                                       application_ref_name: str,
                                       messages: Iterable[openai_chat_types.ChatCompletionMessageParam],
                                       stream: openai.AsyncStream[openai_chat_types.ChatCompletionChunk],
                                       callback: Optional[EvaluateCallback] = None) -> AsyncIterable[ChatCompletionChunk]:
    full_body = ""
    proto_messages = openai_messages_to_proto(messages)
    stream_eval_thread = StreamEvaluationThread()
    stream_eval_thread.start()
    async for chunk in stream:
        if stream_eval_thread.output:
            result: EvaluateResponse = stream_eval_thread.output
            stream_eval_thread.terminate()
            new_stream = maitai.Evaluator.evaluate_realtime(session_id, reference_id, action_type, EvaluationContentType.PARTIAL, proto_messages, application_ref_name, full_body,
                                                            result.evaluation_results[0].description, result.evaluation_results[0].sentinel_id)
            for new_chunk in new_stream:
                yield new_chunk
            return
        maitai_chunk = convert_open_ai_chat_completion_chunk(chunk)
        new_full_body, result_chunk = process_chunk(session_id, reference_id, action_type, application_ref_name, proto_messages, full_body, maitai_chunk, callback)
        if new_full_body != full_body:
            stream_eval_thread.input.append((session_id, reference_id, action_type, EvaluationContentType.PARTIAL, proto_messages, application_ref_name, new_full_body))
        full_body = new_full_body
        if result_chunk is not None:
            yield result_chunk
            break
        yield maitai_chunk
    stream_eval_thread.terminate()


async def _process_inference_stream_async(stream: AsyncIterable[InferenceStreamResponse], callback: EvaluateCallback) -> AsyncIterable[ChatCompletionChunk]:
    last_chat_completion_chunk: Optional[ChatCompletionChunk] = None
    async for infer_resp in stream:
        chunk = process_stream_response(infer_resp, callback, last_chat_completion_chunk)
        if chunk is not None:
            if chunk.choices[0].finish_reason:
                if callback:
                    yield chunk
                    return
                else:
                    last_chat_completion_chunk = chunk
            yield chunk
