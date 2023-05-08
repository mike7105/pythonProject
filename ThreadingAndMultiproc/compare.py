"""тест сравнения времени потоков, процессов, асинхронности"""

import asyncio
import threading
import time
from multiprocessing import Process


def work():
    time.sleep(5)

async def work_async():
    await asyncio.sleep(5)

def thread_create(count):
    print("Start thread_test : ", end="")
    start = time.time()
    list_thread = []
    for x in range(0, count):
        a = threading.Thread(target=work, name=f"Поток {x}", daemon=True)
        list_thread.append(a)
        a.start()
        print(a.name)

    end = time.time()
    print(end - start)
    for x in list_thread:
        x.join()

def process_create(count):
    print("Start process_test : ", end="")
    start = time.time()
    list_thread = []
    for x in range(0, count):
        a = Process(target=work, name=f"Процесс {x}", daemon=True)
        list_thread.append(a)
        a.start()
        print(a.name)

    end = time.time()
    print(end - start)
    for x in list_thread:
        x.join()


def async_create(count):
    print("Start async_test :", end="")
    start = time.time()

    end = 0

    async def main():
        nonlocal end
        tasks = [work_async() for x in range(count)]

        end = time.time()
        return await asyncio.gather(*tasks)

    asyncio.run(main())
    print(end - start)


if __name__ == '__main__':
    count = 20
    async_create(count)  # 0.004005908966064453
    thread_create(count)    # 0.007000446319580078
    process_create(count)   # 0.416546106338501
