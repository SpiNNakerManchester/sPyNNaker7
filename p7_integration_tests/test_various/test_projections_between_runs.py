import spynnaker7.pyNN as sim
from p7_integration_tests.base_test_case import BaseTestCase
# import neo_convertor


def do_run():
    sim.setup(timestep=1)
    pop_1 = sim.Population(1, sim.IF_curr_exp, {}, label="pop_1")
    inp = sim.Population(
        1, sim.SpikeSourceArray, {'spike_times': [[0]]}, label="input")
    sim.Projection(
        pop_1, pop_1, sim.OneToOneConnector(weights=5.0, delays=1))

    pop_1.record("spikes")
    sim.run(20)
    first_spikes = pop_1.getSpikes()

    sim.Projection(
        inp, pop_1, sim.FromListConnector([[0, 0, 5, 5]]))

    sim.reset()
    sim.run(20)
    second_spikes = pop_1.getSpikes()

    return first_spikes, second_spikes


class TestSynapesExcitVsInhib(BaseTestCase):
    def test_run(self):
        first_spikes, second_spikes = do_run()
        assert len(first_spikes) == 0
        assert len(second_spikes) > 0


if __name__ == '__main__':
    first_spikes, second_spikes = do_run()
    print first_spikes
    print second_spikes
