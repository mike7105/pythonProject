"""SuperFastPython.com
example of logging from multiple workers in the multiprocessing pool"""

import logging
from logging.handlers import QueueHandler
from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import current_process
from random import random
from time import sleep


def logger_process(qu: Queue):
    """
    executed in a process that performs logging
    :param Queue qu: общая очередь
    """
    # create a logger
    loggerP = logging.getLogger('app')
    # configure a stream handler
    loggerP.addHandler(logging.StreamHandler())
    # log all messages, debug and up
    loggerP.setLevel(logging.DEBUG)
    # report that the logger process is running
    loggerP.info(f'Logger process running.')
    # run forever
    while True:
        # consume a log message, block until one arrives
        message = qu.get()
        # check for shutdown
        if message is None:
            loggerP.info(f'Logger process shutting down.')
            break
        # log the message
        loggerP.handle(message)


def task(qu: Queue):
    """
    task to be executed in child processes
    :param Queue qu: общая очередь
    """
    # create a logger
    loggerT = logging.getLogger('app')
    # add a handler that uses the shared queue
    loggerT.addHandler(QueueHandler(qu))
    # log all messages, debug and up
    loggerT.setLevel(logging.DEBUG)
    # report initial message
    loggerT.info(f'Child {current_process().name} starting.')
    # simulate doing work
    for i in range(5):
        # report a message
        loggerT.debug(f'Child {current_process().name} step {i}.')
        # block
        sleep(random())
    # report final message
    loggerT.info(f'Child {current_process().name} done.')


# protect the entry point
if __name__ == '__main__':
    # create the manager
    with Manager() as manager:
        # create the shared queue and get the proxy object
        queue = manager.Queue()
        # create a logger
        logger = logging.getLogger('app')
        # add a handler that uses the shared queue
        logger.addHandler(QueueHandler(queue))
        # log all messages, debug and up
        logger.setLevel(logging.DEBUG)
        params: list[tuple] = [(queue, ) for i in range(5)]
        # create the process pool with default configuration
        with Pool() as pool:
            # issue a long-running task to receive logging messages
            _ = pool.apply_async(logger_process, args=(queue,))
            # report initial message
            logger.info('Main process started.')
            # issue task to the process pool
            # results = [pool.apply_async(task, args=(queue,)) for i in range(5)]
            # logger.info('Main process waiting...')
            # for result in results:
            #     result.wait()
            results = pool.starmap_async(task, params)
            # wait for all issued tasks to complete
            logger.info('Main process waiting...')
            for result in results.get():
                logger.info(f'Main process result {result}')
            # report final message
            logger.info('Main process done.')
            # shutdown the long-running logger task
            queue.put(None)
            # close the process pool
            pool.close()
            # wait for all tasks to complete (e.g. the logger to close)
            pool.join()
