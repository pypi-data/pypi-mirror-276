import asyncio
import queue
from typing import Callable, Union

import maitai_gen.chat as chat_types
from maitai_gen.chat import *

ChunkQueue = queue.Queue[Union[chat_types.ChatCompletionChunk, "done"]]
AsyncChunkQueue = asyncio.Queue[Union[chat_types.ChatCompletionChunk, "done"]]


class QueueIterable:
    def __init__(self, chunk_queue: Union[ChunkQueue, AsyncChunkQueue], timeout=None) -> None:
        self.queue = chunk_queue
        self.done = False  # Indicates if "done" token has been received
        self.timeout = timeout

    def __aiter__(self):
        """Returns the asynchronous iterator object itself."""
        return self

    def __iter__(self):
        """Returns the iterator object itself."""
        return self

    def __next__(self) -> chat_types.ChatCompletionChunk:
        """Waits for the next item from the queue or raises StopIteration if "done"."""
        while not self.done:
            try:
                # Wait for an item from the queue, block if necessary
                item = self.queue.get(timeout=self.timeout)  # Wait for 10 seconds, adjust as needed
                if item == "done":
                    self.done = True  # Set done to True to prevent further blocking
                    raise StopIteration
                return item
            except queue.Empty:
                print("Queue timed out")
                self.done = True
                raise TimeoutError
        raise StopIteration

    async def __anext__(self) -> chat_types.ChatCompletionChunk:
        """Waits for the next item from the queue or raises StopAsyncIteration if "done"."""
        if self.done:
            raise StopAsyncIteration

        try:
            # Wait for an item from the queue with a timeout if specified
            if self.timeout:
                item = await asyncio.wait_for(self.queue.get(), timeout=self.timeout)
            else:
                item = await self.queue.get()

            if item == "done":
                self.done = True  # Set done to True to prevent further blocking
                raise StopAsyncIteration

            return item

        except asyncio.TimeoutError:
            print("Queue timed out")
            self.done = True
            raise StopAsyncIteration


EvaluateCallback = Callable[[EvaluateResponse], None]
