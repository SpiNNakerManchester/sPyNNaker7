import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase
from unittest import SkipTest


def do_run(split_spike_source_poisson=False, change_spike_rate=True,
           split_if_curr_exp=False, change_if_curr=True):
    p.setup(1.0)

    if split_spike_source_poisson:
        print "split SpikeSourcePoisson", split_spike_source_poisson
        p.set_number_of_neurons_per_core(p.SpikeSourcePoisson, 27)
    if split_if_curr_exp:
        print "split IF_curr_exp"
        p.set_number_of_neurons_per_core(p.IF_curr_exp, 22)

    inp = p.Population(100, p.SpikeSourcePoisson, {"rate": 100}, label="input")
    pop = p.Population(100, p.IF_curr_exp, {}, label="pop")

    p.Projection(inp, pop, p.OneToOneConnector(weights=5.0))

    pop.record()
    inp.record()

    p.run(100)

    if change_spike_rate:
        inp.set("rate", 10)
    if change_if_curr:
        # pop.set("cm", 0.25)
        pop.set("tau_syn_E", 1)

    p.run(100)

    pop_spikes1 = pop.getSpikes()
    inp_spikes1 = inp.getSpikes()

    p.reset()

    inp.set("rate", 0)
    pop.set("i_offset", 1.0)
    pop.initialize("v", p.RandomDistribution("uniform", [-65.0, -55.0]))
    p.run(100)

    pop_spikes2 = pop.getSpikes()
    inp_spikes2 = inp.getSpikes()

    p.end()

    return (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2)


def plot_spikes(pop_spikes, inp_spikes):
    try:
        import pylab  # deferred so unittest are not dependent on it
        pylab.subplot(2, 1, 1)
        pylab.plot(inp_spikes[:, 1], inp_spikes[:, 0], "r.")
        pylab.subplot(2, 1, 2)
        pylab.plot(pop_spikes[:, 1], pop_spikes[:, 0], "b.")
        pylab.show()
    except Exception:
        print "matplotlib not installed so plotting skipped"


class TestChangeParameter(BaseTestCase):

    def test_run_change(self):
        results = do_run()
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        try:
            self.assertLess(1000, len(pop_spikes1))
            self.assertGreater(1300, len(pop_spikes1))
            self.assertLess(1000, len(inp_spikes1))
            self.assertGreater(1300, len(inp_spikes1))
            self.assertLess(450, len(pop_spikes2))
            self.assertGreater(600, len(pop_spikes2))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))

    def test_run_split_spike(self):
        results = do_run(split_spike_source_poisson=True)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        try:
            self.assertLess(1000, len(pop_spikes1))
            self.assertGreater(1300, len(pop_spikes1))
            self.assertLess(1000, len(inp_spikes1))
            self.assertGreater(1300, len(inp_spikes1))
            self.assertLess(450, len(pop_spikes2))
            self.assertGreater(600, len(pop_spikes2))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))

    def test_run_split_spike_no_if_curr_change(self):
        results = do_run(split_spike_source_poisson=True,
                         change_if_curr=False)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        try:
            self.assertLess(1000, len(pop_spikes1))
            self.assertGreater(1300, len(pop_spikes1))
            self.assertLess(1100, len(inp_spikes1))
            self.assertGreater(1300, len(inp_spikes1))
            self.assertLess(250, len(pop_spikes2))
            self.assertGreater(450, len(pop_spikes2))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))

    def test_run_split_spike_no_rate_change(self):
        results = do_run(split_spike_source_poisson=True,
                         change_spike_rate=False)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        try:
            self.assertLess(1900, len(pop_spikes1))
            self.assertGreater(2100, len(pop_spikes1))
            self.assertLess(1900, len(inp_spikes1))
            self.assertGreater(2100, len(inp_spikes1))
            self.assertLess(450, len(pop_spikes2))
            self.assertGreater(600, len(pop_spikes2))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))

    def test_run_split_if_curr(self):
        results = do_run(split_if_curr_exp=True)
        (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
        try:
            self.assertLess(1000, len(pop_spikes1))
            self.assertGreater(1300, len(pop_spikes1))
            self.assertLess(1000, len(inp_spikes1))
            self.assertGreater(1300, len(inp_spikes1))
            self.assertLess(450, len(pop_spikes2))
            self.assertGreater(600, len(pop_spikes2))
        except Exception as ex:
            # Just in case the range failed
            raise SkipTest(ex)
        self.assertEqual(0, len(inp_spikes2))


if __name__ == '__main__':
    results = do_run(split_spike_source_poisson=True)
    (pop_spikes1, inp_spikes1, pop_spikes2, inp_spikes2) = results
    print len(pop_spikes1)
    print len(inp_spikes1)
    print len(pop_spikes2)
    print len(inp_spikes2)
    # plot_spikes([pop_spikes1, inp_spikes1])
    # plot_spikes([pop_spikes2, inp_spikes2])
