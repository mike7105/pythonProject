"""тест BaseManager в процессах серверная часть"""

import time
from multiprocessing.managers import BaseManager


def get_time():
    """
    возвращает текущее время
    :return: время
    """
    return time.time()


BaseManager.register("get", callable=get_time)
manager = BaseManager(address=('', 4444), authkey=b'abc')
server = manager.get_server()
print("server start")
server.serve_forever()
