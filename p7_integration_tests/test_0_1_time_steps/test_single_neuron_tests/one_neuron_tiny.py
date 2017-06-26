import spynnaker7.pyNN as p
from spynnaker7.pyNN import IF_curr_exp
from p7_integration_tests.base_test_case import BaseTestCase


def do_run():
    CELL_PARAMS_LIF = {'cm': 0.25, 'i_offset': 0.0, 'tau_m': 20.0,
                       'tau_refrac': 2.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
                       'v_reset': -70.0, 'v_rest': -65.0, 'v_thresh': -50.0}

    p.setup(timestep=1, min_delay=1.0, max_delay=144)

    pop = p.Population(1, IF_curr_exp, CELL_PARAMS_LIF, label='pop_1')
    rng = p.NumpyRNG(seed=28375)
    v_init = p.RandomDistribution('uniform', [-60, -40], rng)
    pop.randomInit(v_init)

    p.run(500)


class TestOneNeuronTiny(BaseTestCase):
    """
    tests the get spikes given a simulation at 0.1 ms time steps
    """
    def test_run(self):
        do_run()


if __name__ == '__main__':
    do_run()
