"""код тестирвоания многопроцессорности"""
import random
import time
import multiprocessing
from multiprocessing import Process, Lock, RLock, Array, Queue
from typing import Union
from multiprocessing.pool import Pool


def test1():
    """для запуска внутри процесса"""
    for _ in range(3):
        print(f"[{multiprocessing.current_process().name}] - {time.time()}")
        time.sleep(1)

def get_value(l: Lock):
    """
    функция для теста процесса с блокировщиком
    :param Lock l: блокировщик
    """
    with l:
        pr_name = multiprocessing.current_process().name
        print(f"Процесс [{pr_name}] запущен")

def add_value(locker: Union[RLock, Lock], array: Array, index: int):
    """
    Добавляет случайное значение в массив, затем засыпает на это знаечние
    :param RLock | Lock locker: блокировщик
    :param Array array: массив
    :param int index: индекс массива
    """
    with locker:
        num: int = random.randint(0, 20)
        vtime: str = time.ctime()
        array[index] = num
        print(f"array[{index}] = {num}, time = {vtime}")
        time.sleep(num)

def get_text(q: Queue):
    """
    для теста внутри процесса с очередями
    :param Queue q:
    """
    val: int = random.randint(0, 10)
    q.put(f"{val}")

def get_valueP(value: int):
    """фнукция в процессе
    :return: переданное знаечние
    :param int value: значение цифра
    """
    name = multiprocessing.current_process().name
    print(f"[{name}] value: {value}")
    return value

def testSimpleProc():
    """простой запуск процессов"""
    prc: list = []
    for i in range(3):
        pr: Process = Process(target=test1, name=f"prc-{i}")
        prc.append(pr)
        pr.start()

    # pr.join()  # ждем, пока процесс не будет завершен
    p: Process
    for p in prc:
        p.join()
    print("FINISH!")
    # print(pr.is_alive())
    # print(pr.pid)
    #
    # time.sleep(5)
    # pr.terminate()

class MyProcess(Process):
    """класс с простейшим процессом"""

    def run(self):
        """тело процесса"""
        test1()

def testLockProcess():
    """тест блокировщиков в процессах"""

    lock: Lock = Lock()

    Process(target=get_valueP, args=(lock,)).start()
    Process(target=get_valueP, args=(lock,)).start()

def testArrayProcess():
    """тестирвоание массивов в процессах"""
    arr: Array = Array("i", range(10))
    lock: RLock = RLock()
    processes: list = []

    for i in range(10):
        pr: Process = Process(target=add_value, args=(lock, arr, i,))
        processes.append(pr)
        pr.start()

    p: Process
    for p in processes:
        p.join()

    print(list(arr))

def testQueueProcess():
    """тестирвоание очереди процессов"""
    queue: Queue = Queue()
    processes: list = []

    for _ in range(10):
        pr: Process = Process(target=get_text, args=(queue,))
        processes.append(pr)
        pr.start()

    p: Process
    for p in processes:
        p.join()

    for elem in iter(queue.get, None):
        print(elem)

def end_func(response):
    """коллбек по оончнаию пула процессов
    :param response: знаечние
    """
    print(f"Pool end: {response}")

def out(x, y, z):
    """
    тест внутри процесса с несколькими аргументми
    :param x: арг1
    :param y: арг2
    :param z: арг3
    """
    print(f"value: {x} {y} {z}")
    return x, y, z

def testPoolProcess():
    """тестирвоание пула процессов"""
    print(f"cpu: {multiprocessing.cpu_count()}")

    with Pool(multiprocessing.cpu_count() * 3) as p:
        # p.map(get_valueP, list(range(100)))

        # колбек вызывается после вызова всех функций
        # p.map_async(get_valueP, list(range(100)), callback=end_func)
        # p.close()
        # p.join()

        # вызывается после каждой функции
        # for i in range(10):
        #     p.apply_async(get_valueP, args=(i,), callback=end_func)
        # p.close()
        # p.join()

        # если нужно передать несколько парамтеров
        # p.starmap(out, [(1, 2, 3), (4, 5, 6)])

        # несколкьо парамтеров с колбеком
        p.starmap_async(out, [(1, 2, 3), (4, 5, 6)], callback=end_func)
        p.close()
        p.join()

    print("Finish!")


if __name__ == '__main__':
    # testSimpleProc()
    # mpr: MyProcess = MyProcess()
    # mpr.start()
    # testLockProcess()
    # testArrayProcess()
    # testQueueProcess()
    testPoolProcess()
