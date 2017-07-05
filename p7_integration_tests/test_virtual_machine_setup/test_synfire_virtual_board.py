"""
Synfirechain-like example
"""
import unittest

from p7_integration_tests.base_test_case import BaseTestCase
from p7_integration_tests.scripts.synfire_run import TestRun
from spinnman.exceptions import SpinnmanTimeoutException
from unittest import SkipTest

n_neurons = 200
timestep = 1
max_delay = 14.40
delay = 1.7
neurons_per_core = n_neurons/2
runtime = 500
synfire_run = TestRun()


class TestGetSpikesAt0_1msTimeStep(BaseTestCase):
    """
    tests the get spikes given a simulation at 0.1 ms time steps
    """
    def test_get_spikes(self):
        """
        test for get spikes
        """
        try:
            synfire_run.do_run(n_neurons, time_step=timestep,
                               max_delay=max_delay, delay=delay,
                               neurons_per_core=neurons_per_core,
                               run_times=[runtime])
            spikes = synfire_run.get_output_pop_spikes()
            print spikes
            if len(spikes) != 0:
                raise Exception("Test {} failed as virtual machine is "
                                "producing data".format(__file__))
        # System intentional overload so may error
        except SpinnmanTimeoutException as ex:
            raise SkipTest(ex)


if __name__ == '__main__':
    unittest.main()
