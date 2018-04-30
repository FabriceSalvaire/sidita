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
import sys
import unittest

from sidita import TaskQueue

####################################################################################################

class MyTaskQueue(TaskQueue):

    _logger = logger.getChild('MyTaskQueue')

    ##############################################

    async def task_producer(self):

        N = 10

        for i in range(1, N + 1):
            self._logger.info('Producing {}/{}'.format(i, N))
            # simulate i/o operation using sleep
            # await asyncio.sleep(random.random())
            message = {
                'action': 'run',
                'payload': 'message {}'.format(i),
            }
            await self.submit(message)

        await self.send_stop()

####################################################################################################

class TestTaskQueue(unittest.TestCase):

    ##############################################

    def test(self):

        # sys.path

        task_queue = MyTaskQueue(
            python_path=Path(__file__).resolve().parent,
            worker_module='TestWorker',
            worker_cls='TestWorker',
            max_queue_size=100,
            max_memory=100*1024**2,
            memory_check_interval=timedelta(seconds=5),
            task_timeout=timedelta(seconds=1),
        )
        task_queue.run()

####################################################################################################

if __name__ == '__main__':

    unittest.main()
