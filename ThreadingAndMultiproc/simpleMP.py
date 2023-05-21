"""тривиальный пример"""

import multiprocessing
import math
import random
import time
def sqrt_pandas(x):
    return math.sqrt(x)


if __name__ == '__main__':
    n_proc = multiprocessing.cpu_count()
    lst = [random.randint(1, 10000) for i in range(0, 1000)]
    result = []
    start_time = time.time()
    with multiprocessing.Pool(n_proc) as pool:
        for res in pool.map(sqrt_pandas, lst):
            result.append(res)
    print(time.time()-start_time)