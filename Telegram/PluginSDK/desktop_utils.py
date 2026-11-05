import asyncio
from concurrent.futures import Future
import uuid

from desktop._runtime import context


async def run_on_ui(callback):
    owner = context()
    runtime = owner.manager.runtime
    identity = uuid.uuid4().hex
    future = Future()
    with runtime.lock:
        runtime.ui_calls[identity] = (owner, callback, future)
    try:
        await runtime.request("python_ui", call_id=identity)
        return await asyncio.wrap_future(future)
    finally:
        with runtime.lock:
            runtime.ui_calls.pop(identity, None)


async def run_in_background(callback, *arguments, **keywords):
    return await asyncio.to_thread(callback, *arguments, **keywords)


def create_task(coroutine):
    owner = context()
    return owner.manager.runtime.schedule(owner, coroutine)


def set_timer(delay, callback, *, repeat=False):
    if delay <= 0:
        raise ValueError("Интервал таймера должен быть положительным.")

    async def timer():
        while True:
            await asyncio.sleep(delay)
            result = await run_on_ui(callback)
            if not repeat:
                return result
    return create_task(timer())
