#!/usr/bin/env python
import unittest

import spynnaker7.pyNN as pynn
from spynnaker.pyNN.utilities import globals_variables

class TestPyNNSetup(unittest.TestCase):

    def test_initial_setup(self):
        self.assertEqual(pynn.setup(timestep=1, min_delay=1, max_delay=15.0),
                         0)
        simulator = globals_variables.get_simulator()
        try:
            self.assertEqual(simulator._config.getint("Machine", "machineTimeStep"),
                             1 * 1000)
            self.assertEqual(pynn.get_min_delay(), 1)
            self.assertEqual(pynn.get_max_delay(), 15.0)
        finally:
            pynn.end()

    # def test_setting_up_again(self):
    #     import spynnaker.pyNN as pynn
    #     # self.assertEqual(pynn._spinnaker, None)
    #     pynn.setup(timestep=1.1, min_delay=1.1, max_delay=10.0)
    #     self.assertNotEqual(pynn._spinnaker, None)
    #     pynn.end()
    #     self.assertEqual(pynn._spinnaker, None)


if __name__ == "__main__":
    unittest.main()
