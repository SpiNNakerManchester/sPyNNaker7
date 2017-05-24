#!/usr/bin/env python
import unittest
import spynnaker7.pyNN as pyNN
from spinn_front_end_common.utilities.exceptions import ConfigurationException

cell_params_lif = {'cm': 0.25,
                   'i_offset': 0.0,
                   'tau_m': 20.0,
                   'tau_refrac': 2.0,
                   'tau_syn_E': 5.0,
                   'tau_syn_I': 5.0,
                   'v_reset': -70.0,
                   'v_rest': -65.0,
                   'v_thresh': -50.0}
spike_array = {'spike_times': [0]}
# /Setup


class TestingFixedProbabilityConnector(unittest.TestCase):
    def setUp(self):
        pyNN.setup(timestep=1, min_delay=1, max_delay=10.0)

    def tearDown(self):
        pyNN.end()

    def test_generate_synapse_list_probability_200_percent(self):
        with self.assertRaises(ConfigurationException):
            weight = 2
            delay = 1
            pyNN.FixedProbabilityConnector(2, weight, delay)

    def test_synapse_list_generation_for_negative_sized_populations(self):
        with self.assertRaises(ConfigurationException):
            weight = 2
            delay = 1
            pyNN.FixedProbabilityConnector(-0.5, weight, delay)

if __name__ == "__main__":
    unittest.main()
