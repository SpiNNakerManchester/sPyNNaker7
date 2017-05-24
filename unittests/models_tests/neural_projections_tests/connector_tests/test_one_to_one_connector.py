#!/usr/bin/env python
import unittest
import spynnaker7.pyNN as pyNN

nNeurons = 10
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


class TestingOneToOneConnector(unittest.TestCase):
    def setUp(self):
        pyNN.setup(timestep=1, min_delay=1, max_delay=10.0)

    def tearDown(self):
        pyNN.end()

    def test_connector_populations_of_different_sizes(self):
        weight = 2
        delay = 5
        p1 = pyNN.Population(
            10, pyNN.IF_curr_exp, cell_params_lif, label="pop 1")
        p2 = pyNN.Population(
            5, pyNN.IF_curr_exp, cell_params_lif, label="pop 2")
        j = pyNN.Projection(p1, p2, pyNN.OneToOneConnector(weight, delay))
        self.assertIsNotNone(j)


if __name__ == "__main__":
    unittest.main()
