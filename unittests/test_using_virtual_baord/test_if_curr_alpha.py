import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase


def do_run():
    p.setup(0.1)

    pop_src1 = p.Population(1, p.SpikeSourceArray,
                            {'spike_times': [[5, 15, 20, 30]]}, label="src1")

    pop_ex = p.Population(1, p.IF_curr_alpha, {}, label="test")
    pop_ex.set("tau_syn_E", 2)
    pop_ex.set("tau_syn_I", 4)

    # define the projection
    p.Projection(
        pop_src1, pop_ex, p.OneToOneConnector(weights=1, delays=1),
        target="excitatory")
    p.Projection(
        pop_src1, pop_ex, p.OneToOneConnector(weights=1, delays=20),
        target="inhibitory")

    pop_ex.record()
    pop_ex.record_gsyn()
    pop_ex.record_v()
    p.run(50)

    p.end()


class ParamsSetAsList(BaseTestCase):

    def test_run(self):
        do_run()


if __name__ == '__main__':
    do_run()
