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

from datetime import datetime, timedelta
from pathlib import Path
import asyncio
import asyncio.subprocess
import logging
import os
import sys

import psutil

from .Message import AsyncMessageStream
from .Statistics import DataSetMoment

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def to_MB(x):
    return x/1024**2

####################################################################################################

class WorkerMetrics:

    ##############################################

    def __init__(self, number_of_workers=0):

        self._crash = 0
        self._restart = {i:0 for i in range(number_of_workers)}
        self._memory = {i:DataSetMoment() for i in range(number_of_workers)}
        self._task_time = {i:DataSetMoment() for i in range(number_of_workers)}

    ##############################################

    def add_crash(self):
        self._crash += 1

    ##############################################

    def add_restart(self, worker_id):
        self._restart[worker_id] += 1

    ##############################################

    def add_memory(self, worker_id, memory):

        self._memory[worker_id].fill(memory)

    ##############################################

    def add_task_time(self, worker_id, task_time):

        # if worker_id not in self._task_time:
        #     self._task_time[worker_id] = DataSetMoment()

        self._task_time[worker_id].fill(task_time)

    ##############################################

    def dump_statistics(self):

        text = 'Worker Statistics\n'
        for worker_id in self._task_time.keys():
            memory = self._memory[worker_id]
            task_time = self._task_time[worker_id]
            text += '  Worker @{0}: {1.number_of_entries} Tasks\n'.format(worker_id, task_time)
            text += '    number of restarts: {}\n'.format(self._restart[worker_id])
            if memory.number_of_entries:
                avg_memory = to_MB(memory.mean)
                text += '    avg memory: {:.1f} MB\n'.format(avg_memory)
            if task_time.number_of_entries:
                text += '    avg task time: {0.mean:.3f}s\n'.format(task_time)
            text += '\n'
        text += '  Crash {}'.format(self._crash)
        return text

####################################################################################################

class TaskMetaData:

    LAST_TASK_ID = -1

    ##############################################

    def __init__(self, task):

        self._task = task
        self.LAST_TASK_ID += 1
        self._task_id = self.LAST_TASK_ID
        self._result = None

        self._woker_id = None
        self._submitted_date = datetime.now()
        self._sent_date = None
        self._result_date = None

    ##############################################

    @property
    def task(self):
        return self._task

    @property
    def task_id(self):
        return self._task_id

    @property
    def result(self):
        return self._result

    @property
    def worker_id(self):
        return self._worker_id

    @property
    def submitted_date(self):
        return self._submitted_date

    @property
    def sent_date(self):
        return self._submitted_date

    @property
    def result_date(self):
        return self._submitted_date

    @property
    def task_time(self):
        return self._result_date - self._sent_date

    @property
    def task_time_s(self):
        return (self._result_date - self._sent_date).total_seconds()

    ##############################################

    def submit(self, worker_id):

        self._worker_id = worker_id
        self._sent_date = datetime.now()

    ##############################################

    @result.setter
    def result(self, value):

        self._result = value
        self._result_date = datetime.now()

####################################################################################################

class Manager:

    DEFAULT_WORKER_MAIN = Path(__file__).resolve().parent.joinpath('worker.py')
    DEFAULT_WORKER_MODULE = '.'.join(__name__.split('.')[:-1] + ['Worker']) # Fixme: api tool ?
    DEFAULT_WORKER_CLASS = 'Worker'

    _logger = _module_logger.getChild('Manager')

    ##############################################

    def __init__(self,
                 worker_main=DEFAULT_WORKER_MAIN,
                 python_path=None,
                 worker_module=DEFAULT_WORKER_MODULE,
                 worker_cls=DEFAULT_WORKER_CLASS,
                 number_of_workers=None,
                 max_queue_size=0,
                 max_memory=0,
                 memory_check_interval=timedelta(minutes=1),
    ):

        self._worker_main = worker_main
        self._python_path = python_path
        self._worker_module = worker_module
        self._worker_cls = worker_cls
        self._number_of_workers = number_of_workers or os.cpu_count()
        self._max_queue_size = max_queue_size
        self._max_memory = max_memory
        self._memory_check_interval = memory_check_interval

        self._worker_metrics = WorkerMetrics(self._number_of_workers)

    ##############################################

    @staticmethod
    def _get_event_loop():

        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()

        loop.set_debug(True)

        return loop

    ##############################################

    def run(self):

        loop = self._get_event_loop()
        self._queue = asyncio.Queue(maxsize=self._max_queue_size, loop=loop)

        task_producer = self.task_producer()
        task_consumers = [self._task_consumer(i) for i in range(self._number_of_workers)]

        loop.run_until_complete(asyncio.gather(
            task_producer,
            *task_consumers,
        ))
        loop.close()

        self._logger.info(self._worker_metrics.dump_statistics())

    ##############################################

    async def task_producer(self):

        # self.submit(message)
        # self.send_stop()

        raise NotImplementedError

    ##############################################

    async def submit(self, task):

        task_metadata = TaskMetaData(task)
        self.on_task_submitted(task_metadata)
        await self._queue.put(task_metadata)

    ##############################################

    async def send_stop(self):

        # indicate the producer is done
        self._logger.info('Send stop to workers')
        for i in range(self._number_of_workers):
            await self._queue.put(None)

    ##############################################

    async def _task_consumer(self, worker_id):

        process, message_stream = await self._create_worker(worker_id)
        dead = False
        self._worker_metrics.add_restart(worker_id)

        last_memory_check = datetime.now()

        while True:
            task_metadata = await self._queue.get()
            if task_metadata is None:
                break # no more job to process

            if self._max_memory and not dead:
                now = datetime.now()
                if now - last_memory_check > self._memory_check_interval:
                    last_memory_check = now
                    process_memory = self._get_process_memory(process)
                    if process_memory > self._max_memory:
                        self._logger.info('Worker @{} has reached memory limit {:.1f} > {:.1f} MB'.format(
                            worker_id, to_MB(process_memory), to_MB(self._max_memory)))
                        self._worker_metrics.add_memory(worker_id, process_memory)
                        process.terminate()
                        await asyncio.sleep(1) # Fixme: better ?
                        dead = True

            if dead: # process.returncode is not None
                self._logger.info('Restart Worker @{}'.format(worker_id))
                process, message_stream = await self._create_worker(worker_id)
                dead = False
                self._worker_metrics.add_restart(worker_id)

            task_metadata.submit(worker_id)
            message_stream.send(task_metadata.task)
            self.on_task_sent(task_metadata)

            try:
                task_metadata.result = await message_stream.receive()
                self._worker_metrics.add_task_time(task_metadata.worker_id, task_metadata.task_time_s)
                self.on_result(task_metadata)
            except asyncio.streams.IncompleteReadError:
                if process.returncode is not None:
                    self._worker_metrics.add_crash()
                    self._logger.info('Worker @{} is dead'.format(worker_id))
                    dead = True

        self._logger.info('Exit worker @{}'.format(worker_id))
        if not dead:
            process_memory = self._get_process_memory(process)
            self._worker_metrics.add_memory(worker_id, process_memory)
            try:
                process.terminate()
                await asyncio.sleep(1) # Fixme: better ?
            except ProcessLookupError: # Fixme:
                self._logger.info('Worker was killed @{} {}'.format(worker_id, process.returncode))

    ##############################################

    def _get_process_memory(self, process):

        try:
            process_metrics = psutil.Process(process.pid)
            with process_metrics.oneshot():
                memory_info = process_metrics.memory_full_info()
                process_memory = memory_info.uss
            return process_memory
        except psutil._exceptions.NoSuchProcess: # Fixme:
            return 0

    ##############################################

    async def _create_worker(self, worker_id):

        self._logger.info('Create worker @{}'.format(worker_id))

        command = [
            sys.executable,
            str(self._worker_main),
            '--worker-module', self._worker_module,
            '--worker-class', self._worker_cls,
            '--worker-id', str(worker_id),
            ]
        if self._python_path:
            command += [
                '--python-path', str(self._python_path),
            ]

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )

        message_stream = AsyncMessageStream(process.stdin, process.stdout)

        return process, message_stream

    ##############################################

    def on_task_submitted(self, task_metadata):

        self._logger.info('Submitted task {0.task}'.format(task_metadata))

    ##############################################

    def on_task_sent(self, task_metadata):

        self._logger.info('Task {0.task} sent to @{0.worker_id}'.format(task_metadata))

    ##############################################

    def on_result(self, task_metadata):

        self._logger.info('Result for task {0.task} from @{0.worker_id}\n{0.result}'.format(task_metadata))