import queue
from typing import Callable, Union

import maitai_gen.chat as chat_types
from maitai_gen.chat import EvaluateResponse

ChunkQueue = queue.Queue[Union[chat_types.ChatCompletionChunk, "done"]]


class QueueIterable:
    def __init__(self, chunk_queue: ChunkQueue, timeout=None) -> None:
        self.queue = chunk_queue
        self.done = False  # Indicates if "done" token has been received
        self.timeout = timeout

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


EvaluateCallback = Callable[[EvaluateResponse], None]
