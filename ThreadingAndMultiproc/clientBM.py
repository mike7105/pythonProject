"""клиент Base Manager для использвоания в процессах"""

from multiprocessing.managers import BaseManager


BaseManager.register("get")
manager = BaseManager(address=('127.0.0.1', 4444), authkey=b'abc')
print("client connected")
manager.connect()

res = manager.get()
print(f"result: {res}")
