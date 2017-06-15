"""
Synfirechain-like example
"""
# !/usr/bin/python
import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase
import spynnaker.plot_utils as plot_utils

from unittest import SkipTest


def do_run(nNeurons):

    spike_list = {'spike_times': [11, 22]}
    print spike_list
    p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)


    pop = p.Population(nNeurons, p.SpikeSourceArray, spike_list, label='input')

    pop.record()

    p.run(200)

    spikes = pop.getSpikes(compatible_output=True)

    p.end()

    return spikes


class BigMultiProcessorSpikeSourcePrint(BaseTestCase):

    def test_run_(self):
        nNeurons = 10  # number of neurons in each population
        spikes = do_run(nNeurons)


if __name__ == '__main__':
    nNeurons = 10  # number of neurons in each population
    spikes = do_run(nNeurons)
    plot_utils.plot_spikes(spikes)
    print spikes
