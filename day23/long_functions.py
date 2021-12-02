import numpy as np
import time


def really_hard_task(some_parameter: int) -> float:
    result = np.random.random()
    time.sleep(2.0)
    print(f"finished task crunching {some_parameter} with result {result:.2f}")
    return result