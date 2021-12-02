import asyncio
import time
from concurrent.futures import ProcessPoolExecutor


def std_ding(thread: str, sleep_delay: int):
    """
    Prints a ding message.

    :param thread: type of thread this was called on.
    :param sleep_delay: slept for how long
    """
    time.sleep(sleep_delay)
    print(f"{int(time.time())} >> {thread}: ding running for {sleep_delay} seconds!")


def hard_math(number_size: int):
    time.sleep(number_size // 2)  # pretend to do hard math
    print(f"{int(time.time())} >> Hard math: {number_size}")
    return number_size


async def async_ding(thread: str, sleep_delay: int):
    """
    Prints a ding message.

    :param thread: type of thread this was called on.
    :param sleep_delay: slept for how long
    """
    await asyncio.sleep(sleep_delay)  # any other coro, like a download
    # time.sleep(sleep_delay)
    print(f"{int(time.time())} >> {thread}: ding running for {sleep_delay} seconds!")


async def main_just_tasks():  # coroutine due to the 'async' keyword
    print(f"{int(time.time())} >> START")
    # if it's just short code (runs all in the same thread)
    tasks_main_thread = [asyncio.create_task(async_ding("Main", t))
                         for t in range(10)]

    await asyncio.gather(*tasks_main_thread)  # *tasks_main_thread == tasks_main_thread.unroll()
    return


async def main_plus_threads():
    the_loop = asyncio.get_running_loop()

    tasks_main_thread = [asyncio.create_task(async_ding("Main", t)) for t in range(10)]

    # if we have blocking I/O (None means a thread will be used,
    # do not use this for hard computations)
    tasks_another_thread = [the_loop.run_in_executor(None, std_ding, "Another", t)
                            for t in range(10)]
    await asyncio.gather(*tasks_main_thread, *tasks_another_thread)
    return


async def main_plus_processes():
    the_loop = asyncio.get_running_loop()
    tasks_main_thread = [asyncio.create_task(async_ding("Main", t)) for t in range(10)]

    # if we have hard computation, use multiprocessing (OS-level multitasking)
    with ProcessPoolExecutor(max_workers=6) as ppe:  # Context Manager
        tasks_other_processes = [the_loop.run_in_executor(ppe, hard_math, 5)
                                 for t in range(10)]

        # NOTE: this MUST be tabbed over, or you will be running serially!
        await asyncio.gather(*tasks_main_thread, *tasks_other_processes)
        return


async def main_all():
    with ProcessPoolExecutor(max_workers=6) as ppe:
        the_loop = asyncio.get_running_loop()
        tasks_main_thread = [asyncio.create_task(async_ding("Main Loop", t)) for t in range(10)]
        tasks_another_thread = [the_loop.run_in_executor(None, std_ding, "Separate Thread", t) for t in range(10)]
        tasks_other_processes = [the_loop.run_in_executor(ppe, hard_math, 5) for _ in range(10)]
        await asyncio.gather(*tasks_main_thread, *tasks_another_thread, *tasks_other_processes)
        return


if __name__ == '__main__':
    # asyncio.run(main_just_tasks(), debug=True)
    # asyncio.run(main_plus_threads(), debug=True)
    # asyncio.run(main_plus_processes(), debug=True)
    asyncio.run(main_all())
