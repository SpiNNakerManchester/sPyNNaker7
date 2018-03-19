import unittest

import spynnaker7.pyNN as p
import numpy as np


def distance(x0, x1, grid=np.asarray([16, 16]), type='euclidian'):
    x0 = np.asarray(x0)
    x1 = np.asarray(x1)
    delta = np.abs(x0 - x1)
    delta = np.where(delta > grid * .5, delta - grid, delta)

    if type == 'manhattan':
        return np.abs(delta).sum(axis=-1)
    return np.sqrt((delta ** 2).sum(axis=-1))


def generate_rates(s, grid, f_base=5, f_peak=152.8, sigma_stim=2):
    '''
    Function that generates an array the same shape as the input layer so that
    each cell has a value corresponding to the firing rate for the neuron
    at that position.
    '''
    _rates = np.zeros(grid)

    for x in range(grid[0]):
        for y in range(grid[1]):
            _d = distance(s, (x, y), grid)
            _rates[x, y] = f_base + f_peak * np.e ** (
                -_d / (2 * (sigma_stim ** 2)))
    return _rates

class TestVRPSS(unittest.TestCase):
    def test_variable_rate_poisson_spike_source_generation(self):
        timestep = 1
        interval = 20
        total_runtime = 15000 * interval
        number_of_rates = total_runtime // interval
        num_sources = 256
        p.setup(timestep)


        grid = np.asarray((1, 256))
        rates = []
        max_locs = []
        for i in range(number_of_rates):
            x = np.random.randint(0, 256)
            max_locs.append(x)
            rate = generate_rates([1, x], grid)
            rates.append(list(rate[0]))


        ext_stim = p.Population(
            num_sources, p.SpikeSourcePoissonVariable,
            {'rate_interval_duration': interval, 'rate': rates},
            label="expoisson")

        exc_pop = p.Population(num_sources, p.IF_curr_exp, {})

        p.Projection(ext_stim, exc_pop,
                     p.OneToOneConnector(weights=2, delays=timestep))

        recording = True
        if recording:
            ext_stim.record()

        p.run(total_runtime)

        if recording:
            source_spikes = ext_stim.getSpikes()
            self.assertTrue(source_spikes is not None
                            and len(source_spikes) > 0)
        p.end()

