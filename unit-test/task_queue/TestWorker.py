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
logger = sidita.Logging.setup_logging('sidita-worker')

####################################################################################################

import numpy as np
import logging
import random
import sys
import time

from sidita.Worker import Worker

####################################################################################################

class TestWorker(Worker):

    _logger = logger.getChild('Worker')

    ##############################################

    def __init__(self, worker_id):

        super().__init__(worker_id)

        self._pool = []

    ##############################################

    def on_task(self, task):

        # simulate workload
        # time.sleep(random.random()/1000)
        # time.sleep(random.random()*10)

        # simulate crash
        # if random.random() < .1:
        #     1/0

        # simulate memory load
        # self._pool.append(np.ones(1024*100))

        return {
            'status': 'completed',
            'payload': task['payload'],
        }
