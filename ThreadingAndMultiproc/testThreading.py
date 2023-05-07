"""Код тестирования многопоточности"""

from typing import Any
import time
import random
import threading
from threading import Thread, Lock, RLock, Timer, local, BoundedSemaphore, Barrier

def testSimpleThread():
    """
    функция для тетсирвоаняи простейших вариантов потока
    """
    def test(data: Any):
        """
        функция с бесокнечным циклом для выполнения в потоке
        :param Any data: любые данные
        """
        while True:
            print(f"[{threading.current_thread().name}] - {data}")
            time.sleep(1)

    thr = Thread(target=test, args=(str(time.ctime()),), name="thr-1")
    thr.start()  # не блочит дальнейший поток выполнения

    print(f"main thread name: {threading.main_thread().name}")
    threading.main_thread().name = "MAINTHREAD"
    print(f"main thread name: {threading.main_thread().name}")

    for i in range(50):
        print(f"i={i}")
        time.sleep(1)

        if i % 10 == 0:
            print(f"active thread: {threading.active_count()}")
            print(f"enumerate: {threading.enumerate()}")
            print(f"thr-1 is alive: {thr.is_alive()}")


def testSimpleJoinThread():
    """
    функция для тетсирвоаняи простейших вариантов потока с ожиданием
    """
    def test(data: Any, value: int):
        """
        функция с бесокнечным циклом для выполнения в потоке
        :param int value: кол-во выполнения
        :param Any data: любые данные
        """
        for _ in range(value):
            print(f"[{threading.current_thread().name}] - {data}")
            time.sleep(1)

    thr_list: list[Thread] = []

    for i in range(3):
        thr: Thread = Thread(target=test, args=(str(time.ctime()), i + 1,), name=f"thr-{i}")
        thr_list.append(thr)
        thr.start()

    thr: Thread
    for thr in thr_list:
        thr.join()  # ждет завершения всех потоков

    print(f"finish!")


def testSimpleDaemonThread():
    """
    функция для тетсирвоаняи простейших вариантов потока демона
    демоны потоки завершаются вмсете с завершением программы
    """

    def test(data: Any):
        """
        функция с бесокнечным циклом для выполнения в потоке
        :param Any data: любые данные
        """
        for _ in range(5):
            print(f"[{threading.current_thread().name}] - {data}")
            time.sleep(1)

    thr: Thread = Thread(target=test, args=(str(time.ctime()),), name=f"thr-1", daemon=True)
    # thr.daemon = True
    thr.start()
    time.sleep(1)
    print(f"finish!")


def testLockThread():
    """
    функция тестирует блокирвоки ресурсов в потоке
    """
    value = 0
    # locker: Lock = Lock()  # может быть разблокирован из любого потока
    locker: RLock = RLock()  # НЕ может быть разблокирован из любого потока

    def inc_value():
        """
        увеличивает знаечние value на 1 в бесконченом цикле
        """
        nonlocal value
        while True:
            with locker:
                value += 1
                time.sleep(0.01)
                print(value)

    for _ in range(5):
        Thread(target=inc_value).start()


def testTimerThread():
    """
    функция тестирует запуск по таймеру потока
    """

    def test():
        """
        функция с бесокнечным циклом для выполнения в потоке
        """
        while True:
            print("TEST")
            time.sleep(1)

    thr: Timer = Timer(5, test)
    # thr.daemon = True
    thr.start()  # запускатеся через 5 секунд

    for _ in range(6):
        print("111")
        time.sleep(1)

    # thr.cancel()  # можно отменить до начала выполнения
    print("finish")


def testLocalThread():
    """
    функция тестирует локальные ресурсы потока
    """

    data: local = local()

    def get():
        """
        печатает данные
        """
        print(f"{data.value}")

    def t1():
        """
        функция для первого потока устанавливает данные
        """
        data.value = 111
        get()

    def t2():
        """
        функция для второго поток аустанавливает данные
        """
        data.value = 222
        get()

    Thread(target=t1).start()
    Thread(target=t2).start()


def testSemaphoreThread():
    """тестируем семафоры в потоках, ограничвает кол-во однолврменно выполняемых потоков
    следующий запускатеся ка ктолько освобождается место"""

    max_connections: int = 5
    pool: BoundedSemaphore = BoundedSemaphore(value=max_connections)

    def test():
        with pool:
            slp: int = random.randint(1, 10)
            print(f"[{threading.current_thread().name}] - sleep ({slp})")
            time.sleep(slp)

    for i in range(10):
        Thread(target=test, name=f"thr-{i}").start()


def testBarrierThread():
    """тестирую барьеры в потоках, продолжается когда завершатся все потоки из барьера"""

    locker: Lock = Lock()

    def test(barrier: Barrier):
        slp: int = random.randint(10, 15)
        time.sleep(slp)
        with locker:
            print(f"[{threading.current_thread().name}] start {time.ctime()}")

        barrier.wait()
        with locker:
            print(f"[{threading.current_thread().name}] barrier at {time.ctime()}")

    bar: Barrier = Barrier(5)
    for i in range(10):
        Thread(target=test, args=(bar, ), name=f"thr-{i}").start()


if __name__ == '__main__':
    # testSimpleThread()
    # testSimpleJoinThread()
    # testSimpleDaemonThread()
    # testLockThread()
    # testTimerThread()
    # testLocalThread()
    # testSemaphoreThread()
    testBarrierThread()
