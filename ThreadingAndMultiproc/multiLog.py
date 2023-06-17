""" SuperFastPython.com
example of logging from multiple processes in a process-safe manner"""

import logging
from logging.handlers import QueueHandler
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import current_process
from random import random
from time import sleep


def logger_process(qu: Queue):
    """
    executed in a process that performs logging
    :param Queue qu: Общая очередь
    """
    # create a logger
    loggerPr = logging.getLogger('app')
    # configure a stream handler
    loggerPr.addHandler(logging.StreamHandler())
    # log all messages, debug and up
    loggerPr.setLevel(logging.DEBUG)
    # run forever
    while True:
        # consume a log message, block until one arrives
        message = qu.get()
        # check for shutdown
        if message is None:
            break
        # log the message
        loggerPr.handle(message)


def task(qu: Queue):
    """
    task to be executed in child processes
    :param Queue qu: Общая очередь
    """
    # create a logger
    loggerT = logging.getLogger('app')
    # add a handler that uses the shared queue
    loggerT.addHandler(QueueHandler(qu))
    # log all messages, debug and up
    loggerT.setLevel(logging.DEBUG)
    # get the current process
    proc = current_process()
    # report initial message
    loggerT.info(f'Child {proc.name} starting.')
    # simulate doing work
    for i in range(5):
        # report a message
        loggerT.debug(f'Child {proc.name} step {i}.')
        # block
        sleep(random())
    # report final message
    loggerT.info(f'Child {proc.name} done.')


if __name__ == '__main__':
    # create the shared queue
    queue = Queue()
    # create a logger
    logger = logging.getLogger('app')
    # add a handler that uses the shared queue
    logger.addHandler(QueueHandler(queue))
    # log all messages, debug and up
    logger.setLevel(logging.DEBUG)
    # start the logger process
    logger_p = Process(target=logger_process, args=(queue,))
    logger_p.start()
    # report initial message
    logger.info('Main process started.')
    # configure child processes
    processes = [Process(target=task, args=(queue,)) for i in range(5)]
    # start child processes
    for process in processes:
        process.start()
    # wait for child processes to finish
    for process in processes:
        process.join()

    # report final message
    logger.info('Main process done.')
    # shutdown the queue correctly
    queue.put(None)
