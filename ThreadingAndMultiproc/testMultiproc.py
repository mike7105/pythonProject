"""код тестирвоания многопроцессорности"""

import time
import multiprocessing
from multiprocessing import Process

def test1():
    """для запуска внутри процесса"""
    for _ in range(3):
        print(f"[{multiprocessing.current_process().name}] - {time.time()}")
        time.sleep(1)

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


if __name__ == '__main__':
    # testSimpleProc()
    mpr: MyProcess = MyProcess()
    mpr.start()
