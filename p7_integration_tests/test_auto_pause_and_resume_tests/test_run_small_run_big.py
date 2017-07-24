import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase


def do_run():
    p.setup(timestep=1)
    pop_1 = p.Population(1, p.IF_curr_exp, {}, label="pop_1")
    input = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]},
                         label="input")
    p.Projection(input, pop_1, p.OneToOneConnector(weights=5.0, delays=1),
                 target="excitatory")
    p.Projection(pop_1, pop_1, p.OneToOneConnector(weights=5.0, delays=1),
                 target="excitatory")

    pop_1.record()
    p.run(20)
    spikes1 = pop_1.getSpikes()
    p.run(20)
    spikes2 = pop_1.getSpikes()
    p.run(100)
    spikes3 = pop_1.getSpikes()
    return (spikes1, spikes2, spikes3)


class TestRunSmallRunBig(BaseTestCase):
    """
    tests the printing of get gsyn given a simulation
    """

    def test_get_gsyn(self):
        (spikes1, spikes2, spikes3) = do_run()
        self.assertEquals(2, len(spikes1))
        self.assertEquals(5, len(spikes2))
        self.assertEquals(19, len(spikes3))


if __name__ == '__main__':
    (spikes1, spikes2, spikes3) = do_run()
    print spikes3
