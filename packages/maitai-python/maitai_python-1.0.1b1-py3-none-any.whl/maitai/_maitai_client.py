import asyncio
import os
import threading


class MaiTaiClient:
    MAITAI_HOST = os.environ.get("MAITAI_HOST", 'https://api.trymaitai.ai')

    def __init__(self):
        super().__init__()

    @classmethod
    def run_async(cls, coro):
        """
        Modified helper method to run coroutine in a background thread if not already in an asyncio loop,
        otherwise just run it. This allows for both asyncio and non-asyncio applications to use this method.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # No running event loop
            loop = None

        if loop and loop.is_running():
            # We are in an asyncio loop, schedule coroutine execution
            asyncio.create_task(coro, name='maitai')
        else:
            # Not in an asyncio loop, run in a new event loop in a background thread
            def run():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                new_loop.run_until_complete(coro)
                new_loop.close()

            threading.Thread(target=run).start()
