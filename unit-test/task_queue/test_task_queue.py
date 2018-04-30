####################################################################################################
#
# sidita - Simple Distributed Task Queue
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import sidita.Logging
logger = sidita.Logging.setup_logging('sidita')

####################################################################################################

from datetime import timedelta
from pathlib import Path
import random
import unittest

from sidita import TaskQueue, TaskState
from sidita.Units import u_MB

####################################################################################################

class MyTaskQueue(TaskQueue):

    _logger = logger.getChild('MyTaskQueue')

    ##############################################

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._tasks = {}

    ##############################################

    def __iter__(self):
        return iter(self._tasks.values())

    ##############################################

    async def task_producer(self):

        N = 10

        for i in range(1, N + 1):
            self._logger.info('Producing {}/{}'.format(i, N))
            # simulate workload
            # await asyncio.sleep(random.random())
            task = {
                'action': 'run',
                'payload': 'message {}'.format(i),
            }
            await self.submit(task)

        await self.send_stop()

    ##############################################

    def on_task_submitted(self, task_metadata):

        super().on_task_submitted(task_metadata)
        self._tasks[task_metadata.id] = task_metadata

    ##############################################

    def on_task_sent(self, task_metadata):

        super().on_task_sent(task_metadata)

    ##############################################

    def on_result(self, task_metadata):

        super().on_result(task_metadata)

    ##############################################

    def on_timeout_error(self, task_metadata):

        pass

    ##############################################

    def on_stream_error(self, task_metadata):

        pass

####################################################################################################

class TestTaskQueue(unittest.TestCase):

    ##############################################

    def test(self):

        task_queue = MyTaskQueue(
            python_path=Path(__file__).resolve().parent,
            worker_module='TestWorker', # cannot define TestWorker in unit-test file
            worker_cls='TestWorker',
            max_queue_size=100,
            max_memory=100@u_MB,
            memory_check_interval=timedelta(seconds=5),
            task_timeout=timedelta(seconds=1),
        )
        task_queue.run()

        for task in task_queue:
            self.assertEqual(task.state, TaskState.READY)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
