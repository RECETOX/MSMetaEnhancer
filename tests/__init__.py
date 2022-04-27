import asyncio
import sys

if sys.platform == 'win32':
    # Set the policy to prevent "Event loop is closed" error on Windows - https://github.com/encode/httpx/issues/914
    # See https://stackoverflow.com/questions/63860576/asyncio-event-loop-is-closed-when-using-asyncio-run
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
