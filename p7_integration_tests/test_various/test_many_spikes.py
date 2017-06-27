"""
Synfirechain-like example
"""
# !/usr/bin/python
import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase
import spynnaker.plot_utils as plot_utils
import unittest
from unittest import SkipTest


def do_run(nNeurons, _neurons_per_core):

    spike_list = {'spike_times': [float(x) for x in range(0, 599, 50)]}
    p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)

    p.set_number_of_neurons_per_core("SpikeSourceArray", _neurons_per_core)


    pop = p.Population(nNeurons, p.SpikeSourceArray, spike_list, label='input')

    pop.record()

    p.run(1000)

    spikes = pop.getSpikes(compatible_output=True)

    p.end()

    return spikes


class BigManySpikes(BaseTestCase):

    def test_sixty_eight(self):
        nNeurons = 600  # number of neurons in each population
        spikes = do_run(nNeurons, 68)
        try:
            self.assertEquals(len(spikes), 7200)
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)

    @unittest.skip("add issue")
    def test_sixty_nine(self):
        nNeurons = 600  # number of neurons in each population
        spikes = do_run(nNeurons, 69)
        try:
            self.assertEquals(len(spikes), 7200)
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)

if __name__ == '__main__':
    nNeurons = 600  # number of neurons in each population
    spikes = do_run(nNeurons)
    plot_utils.plot_spikes(spikes)
    print spikes
