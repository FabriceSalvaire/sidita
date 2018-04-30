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

import unittest

from sidita.Units import *

####################################################################################################

class TestUnits(unittest.TestCase):

    ##############################################

    def test(self):

        self.assertEqual(int(1@u_kB), 1024**1)
        self.assertEqual(int(1@u_MB), 1024**2)
        self.assertEqual(int(1@u_GB), 1024**3)
        self.assertEqual(int(1@u_TB), 1024**4)
        self.assertEqual(int(1@u_PB), 1024**5)

        self.assertEqual(int(1@u_kB * 10), 1024*10)
        self.assertEqual(int(10 * 1@u_kB), 1024*10)
        unit = 1@u_kB
        unit *= 10
        self.assertEqual(int(unit), 1024*10)

        self.assertEqual((1@u_MB) / (1@u_kB), 1024)

        self.assertEqual(int(1@u_min), 60)
        self.assertEqual(int(1@u_hour), 60*60)
        self.assertEqual(int(1@u_day), 24*60*60)

        self.assertEqual(float(1@u_min * 2.1), 60 * 2.1)
        unit = 1@u_min
        unit *= 2.1
        self.assertEqual(int(unit), 60*2.1)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
