import time
import json
import asyncio


def begin_task_execution(async_func):
    def wrap(*args, **kwargs):
        return asyncio.run(async_func(*args, **kwargs))

    return wrap


def load_json_buffer(string):
    try:
        return json.loads(string)
    except json.JSONDecodeError:
        return None


def time_api(func):
    """
    Decorator to measure the execution time of a function.
    """

    def time_wrapper(*args, **kwargs):
        """
        Passed function reference is utilized to run the function with its
        original arguments while maintaining timing and logging functions.
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} executed in {elapsed_time:.4f} seconds.")
        return result

    # We return the augmented function's reference.
    return time_wrapper
