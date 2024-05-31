import functools
import inspect
from typing import Any, Callable, Sequence, TypeVar, Union

import openai.types.chat as openai_types

import maitai_gen.chat as chat_types
from maitai_gen.chat import EvaluateResponse

CallableT = TypeVar("CallableT", bound=Callable[..., Any])


def required_args(*variants: Sequence[str]) -> Callable[[CallableT], CallableT]:
    def inner(func: CallableT) -> CallableT:
        params = inspect.signature(func).parameters
        positional = [
            name
            for name, param in params.items()
            if param.kind
               in {
                   param.POSITIONAL_ONLY,
                   param.POSITIONAL_OR_KEYWORD,
               }
        ]

        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            given_params: set[str] = set()
            for i, _ in enumerate(args):
                try:
                    given_params.add(positional[i])
                except IndexError:
                    raise TypeError(
                        f"{func.__name__}() takes {len(positional)} argument(s) but {len(args)} were given"
                    ) from None

            for key in kwargs.keys():
                given_params.add(key)

            for variant in variants:
                matches = all((param in given_params for param in variant))
                if matches:
                    break
            else:  # no break
                if len(variants) > 1:
                    variations = human_join(
                        ["(" + human_join([quote(arg) for arg in variant], final="and") + ")" for variant in variants]
                    )
                    msg = f"Missing required arguments; Expected either {variations} arguments to be given"
                else:
                    assert len(variants) > 0

                    # TODO: this error message is not deterministic
                    missing = list(set(variants[0]) - given_params)
                    if len(missing) > 1:
                        msg = f"Missing required arguments: {human_join([quote(arg) for arg in missing])}"
                    else:
                        msg = f"Missing required argument: {quote(missing[0])}"
                raise TypeError(msg)
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return inner


# copied from https://github.com/Rapptz/RoboDanny
def human_join(seq: Sequence[str], *, delim: str = ", ", final: str = "or") -> str:
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


def quote(string: str) -> str:
    """Add single quotation marks around the given string. Does *not* do any escaping."""
    return f"'{string}'"


def convert_openai_chat_completion(chat: openai_types.ChatCompletion) -> chat_types.ChatCompletionResponse:
    return chat_types.ChatCompletionResponse().from_dict(chat.to_dict())


def set_completion_evaluation_response(completion: chat_types.ChatCompletionResponse, response: EvaluateResponse):
    completion.evaluate_response = response
    try:
        completion.choices[0].message.content = response.evaluation_results[0].meta["correction_pre"]
        completion.original_choices = [_copy_choice(choice) for choice in completion.choices]
    except:
        pass


def _copy_choice(choice: Union[openai_types.chat_completion.Choice, chat_types.ChatCompletionChoice]) -> chat_types.ChatCompletionChoice:
    message = chat_types.ChatMessage(content=choice.message.content, role=choice.message.role)
    copied_choice = chat_types.ChatCompletionChoice(finish_reason=choice.finish_reason, index=choice.index,
                                                    logprobs=choice.logprobs, message=message)
    return copied_choice


def set_chunk_evaluation_response(chunk: chat_types.ChatCompletionChunk, response: EvaluateResponse):
    chunk.evaluate_response = response


def convert_open_ai_chat_completion_chunk(chunk: openai_types.ChatCompletionChunk) -> chat_types.ChatCompletionChunk:
    return chat_types.ChatCompletionChunk().from_dict(chunk.to_dict())
