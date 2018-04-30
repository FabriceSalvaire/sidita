.. include:: project-links.txt
.. include:: abbreviation.txt

.. _first-steps-page:

=========================
 First Steps with Sidita
=========================

First we will implement our task queue in the file :file:`TestTaskQueue.py`.

.. code-block:: py3

    # import sidita.Logging
    # logger = sidita.Logging.setup_logging('sidita')

    # import random

    from sidita import TaskQueue

    class TestTaskQueue(TaskQueue):

        # _logger = logger.getChild('TestTaskQueue')


        # def __init__(self, *args, **kwargs):
        #    super().__init__(*args, **kwargs)


        async def task_producer(self):
	    """Custom coroutine method to sumbit tasks"""
   	    # this method is a coroutine, cf. async def and await
	    # it runs within an asyncio event loop
            for i in range(10):
                # self._logger.info('Producing {}/{}'.format(i, N))

                # simulate workload
                # await asyncio.sleep(random.random())

		# We can submit any pickable object
                task = {
                    'action': 'run',
                    'payload': 'message {}'.format(i),
                }
                await self.submit(task) # we await on asyncio queue.put

	    # stop workers
            await self.send_stop() # in fact submit None * number_of_workers


        # Custom signal handlers

        def on_task_submitted(self, task_metadata):
            super().on_task_submitted(task_metadata)

        def on_task_sent(self, task_metadata):
            super().on_task_sent(task_metadata)

        def on_result(self, task_metadata):
            super().on_result(task_metadata)

        def on_timeout_error(self, task_metadata):
            pass

        def on_stream_error(self, task_metadata):
            # worker likely crashed
            pass


Then we implement our worker in the file :file:`TestWorker.py`

.. code-block:: py3

    # import sidita.Logging
    # logger = sidita.Logging.setup_logging('sidita-worker')

    # import numpy as np
    # import logging
    # import random
    import sys
    # import time

    from sidita import Worker

    class TestWorker(Worker):

        # _logger = logger.getChild('Worker')


        # def __init__(self, worker_id):
        #     super().__init__(worker_id)
        #     self._pool = []


        def on_task(self, task):
	    """Custom method to handle task."""

            # simulate workload
            # time.sleep(random.random()/1000)
            # time.sleep(random.random()*10)

            # simulate crash
            # if random.random() < .1:
            #     1/0

            # simulate memory load
            # self._pool.append(np.ones(1024*100))

	    # Result can be any pickable object
            return {
                'status': 'completed',
                'payload': task['payload'],
            }


Finally we will write the code to run our task queue.

.. code-block:: py3

    from datetime import timedelta
    from pathlib import Path

    from sidita.Units import u_MB

    from TestTaskQueue import TestTaskQueue

    task_queue = TestTaskQueue(
        # Set the worker implementation : Python Path / worker_module . worker_cls
        python_path=Path(__file__).resolve().parent, # optional path to find our worker_module
        worker_module='TestWorker',
        worker_cls='TestWorker',

        max_queue_size=100, # to limit memory pressure, producer will be blocked when the queue is full

	# Worker sanity check
        max_memory=100@u_MB, # bytes
        memory_check_interval=timedelta(seconds=5),
        task_timeout=timedelta(seconds=1),
    )
    task_queue.run() # start asyncio event loop until all tasks are done
