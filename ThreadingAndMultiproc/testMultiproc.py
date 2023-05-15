"""код тестирвоания многопроцессорности"""
import random
import time
import multiprocessing
from multiprocessing import Process, Lock, RLock, Array, Queue, Event, Condition, Barrier, Manager, Pipe
from typing import Union
from multiprocessing.sharedctypes import Array as Arr
from multiprocessing.pool import Pool
from multiprocessing.synchronize import Event as Eve
from multiprocessing.synchronize import Condition as Cond
from multiprocessing.synchronize import Barrier as Bar
from multiprocessing.managers import SyncManager as Man, BaseManager


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

def testE(event: Eve):
    """тестирвоание в потоке с ивентом"""
    print("testE start")
    while True:
        event.wait()
        print("test")
        time.sleep(1)

def test_Event(event: Eve):
    """разблокирвока и блокировка ивента"""
    while True:
        time.sleep(5)
        event.set()
        print("Event True")
        time.sleep(5)
        event.clear()
        print("Event False")

def testEventProcess():
    event: Eve = Event()
    Process(target=testE, args=(event,)).start()
    Process(target=test_Event, args=(event,)).start()

def f1(cond: Cond):
    """для условий в процессе"""
    print("Start f1")
    while True:
        with cond:
            cond.wait()
            print("получили событие")

def f2(cond: Cond):
    """посылает сигнал для f1 в процесс"""
    for i in range(100):
        if i % 10 == 0:
            with cond:
                cond.notify()
        else:
            print(f"f2: {i}")

        time.sleep(1)

def testConditionProcess():
    """тестирвоанеи условий в процессе -- после срабатывания онуляется. нужно каждый раз разблокировтаь"""
    cond: Cond = Condition()
    Process(target=f1, args=(cond,)).start()
    Process(target=f2, args=(cond,)).start()

def f1b(bar: Bar):
    """функция в процессе с барьером"""
    name = multiprocessing.current_process().name
    sl = random.randint(2, 10)
    print(f"[{name}] - sleep {sl} sec!")
    time.sleep(sl)
    bar.wait()  # ждем пока закончатся все процецессы из барьера
    print(f"[{name}] - start!!")

def testBarrierProcess():
    """тестирование барьеров в процессах"""
    b: Bar = Barrier(5)
    for i in range(10):
        Process(target=f1b, args=(b,)).start()

def f1m(m_dict: dict, m_array: list):
    """функция внутри процессов с менеджером"""
    m_dict["name"] = "test"
    m_dict["version"] = "1.8"
    m_array.append(1)
    m_array.append(2)

def testManagerProcess():
    """тестирвоание менеджеров в процессах"""
    m: Man
    with Manager() as m:
        d = m.dict()
        l = m.list()
        pr = Process(target=f1m, args=(d, l,))
        pr.start()
        pr.join()

        print(f"dict: {d}")
        print(f"list: {l}")

def send_data(conn):
    """передача данных в процессах"""
    conn.send("hello world")
    # conn.close()

def send_data2(conn):
    """передача данных в процессах"""
    conn.send("hello 2")
    # conn.close()

def getter(pipe: Pipe):
    """принимает данные из трубы"""
    out, inp = pipe
    inp.close()
    while True:
        try:
            print(f"data: {out.recv()}")
        except:
            print(f"exception")
            break

def setter(sequence, inp):
    """устанавливает данные в трубе"""
    for item in sequence:
        time.sleep(0.4)
        inp.send(item)


def testPipeProcess():
    """передача  информации между процессами через труды"""
    output_c, input_c = Pipe()
    # p = Process(target=send_data, args=(input_c, ))
    # p.start()
    # p.join()

    # Process(target=send_data, args=(input_c,)).start()
    # Process(target=send_data2, args=(input_c,)).start()
    # print(f"data: {output_c.recv()}")
    # print(f"data: {output_c.recv()}")
    # print(f"data: {output_c.recv()}")

    g = Process(target=getter, args=((output_c, input_c),))
    g.start()

    setter([1, 2, 3, 4, 5], input_c)
    output_c.close()
    input_c.close()


if __name__ == '__main__':
    # testSimpleProc()
    # mpr: MyProcess = MyProcess()
    # mpr.start()
    # testLockProcess()
    # testArrayProcess()
    # testQueueProcess()
    # testPoolProcess()
    # testEventProcess()
    # testConditionProcess()
    # testBarrierProcess()
    # testManagerProcess()
    testPipeProcess()
