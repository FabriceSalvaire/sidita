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

import numpy as np
import logging
import random
import sys
import time

from .Message import StandardMessageStream

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Worker:

    _logger = _module_logger.getChild('Worker') # Fixme: must write to stderr

    ##############################################

    def __init__(self, worker_id):

        self._worker_id = worker_id

    ##############################################

    def run(self):

        self._logger.info('Start Worker @{}'.format(self._worker_id))

        message_stream = StandardMessageStream(
            input_stream=sys.stdin,
            output_stream=sys.stdout,
        )

        self._pool = []

        while True:
            message = message_stream.receive()
            self._logger.info('Worker @{} received {}'.format(self._worker_id, message))
            time.sleep(random.random()/1000)
            # if random.random() < .1:
            #     1/0
            self._pool.append(np.ones(1024*100))
            message = {
                'status': 'completed',
                'payload': message['payload'],
            }
            message_stream.send(message)