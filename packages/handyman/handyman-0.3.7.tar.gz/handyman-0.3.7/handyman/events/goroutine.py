import asyncio
from threading import Thread

# Getting loop.
try:
    _goroutine_loop = asyncio.get_event_loop()
except:
    _goroutine_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_goroutine_loop)


def _run() -> None:
    '''
    Start loop.
    '''
    _goroutine_loop.run_forever()


def go(obj: callable, *args) -> None:
    '''
    Run a coroutine or a func asynchronously.
    Easy concurrency in Python.
    Args:
        obj: Takes coroutine function as object.
        *args: Arguments for your obj.
               You can also use functools.partial() for your func.
    Return:
        None
    '''
    # If a coroutine function run this.
    if callable(obj) and asyncio.iscoroutinefunction(obj):
        future = asyncio.run_coroutine_threadsafe(obj(*args), _goroutine_loop)
    else:
        raise TypeError('A coroutine function object is required')


# Run the loop in a thread.
T = Thread(target=_run, daemon=True)
T.start()
