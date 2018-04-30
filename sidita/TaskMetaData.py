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

__all__ = [
    'TaskMetaData',
]

####################################################################################################

from datetime import datetime

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
