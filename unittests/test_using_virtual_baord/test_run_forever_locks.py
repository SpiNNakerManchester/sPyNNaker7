from spinn_front_end_common.utilities.exceptions import ConfigurationException

import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase


def setup(runtime):
    try:
        p.end()
    except ConfigurationException:
        pass
    p.setup(timestep=1)
    pop_1 = p.Population(1, p.IF_curr_exp, {}, label="pop_1")
    input = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]},
                         label="input")
    input_proj = p.Projection(input, pop_1,
                              p.OneToOneConnector(weights=5.0, delays=1),
                              target="excitatory")
    assert input_proj is not None
    p.run(runtime)
    return (pop_1, input, input_proj)


class Test_run_forever(BaseTestCase):

    def test_run_run_normal(self):
        (pop_1, input, input_proj) = setup(10)
        pop_1.set("tau_m", 20)
        pop_1.tset("tau_m", [20])
        pop_1.initialize("v", 20)
        p.run(10)
        p.reset()
        pop_1.randomInit(20)

    def test_forever_run(self):
        setup(None)
        with self.assertRaises(ConfigurationException):
           p.run(10)

    def test_forever_reset(self):
        setup(None)
        with self.assertRaises(ConfigurationException):
           p.reset()

    def test_forever_population(self):
        setup(None)
        with self.assertRaises(ConfigurationException):
            pop_2 = p.Population(1, p.IF_curr_exp, {}, label="pop_2")

    def test_forever_projection(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            p.Projection(input, pop_1,
                         p.OneToOneConnector(weights=5.0, delays=1),
                         target="excitatory")

    def test_forever_set(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            pop_1.set("tau_m", 20)

    def test_forever_tset(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            pop_1.tset("tau_m", [20])

    def test_forever_initialize(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            pop_1.initialize("v", 20)

    def test_forever_randomInit(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            pop_1.randomInit(20)

    def test_forever_record(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            pop_1.record()

    def test_forever_record_v(self):
        (pop_1, input, input_proj) = setup(None)
        with self.assertRaises(ConfigurationException):
            pop_1.record_v()

if __name__ == '__main__':
    pass

