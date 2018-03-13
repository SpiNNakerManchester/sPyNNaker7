import unittest
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_base import IFCurrExpBase


class TestIFCurrExpModel(unittest.TestCase):
    @unittest.skip("unittests/models_tests/neuron_model_tests/"
                   "test_izk_curr_exp_model.py "
                   "test_new_izk_curr_exp_mode")
    def test_new_if_curr_exp_model(self):
        # pylint: disable=protected-access
        cell_params_lif = {'cm': 0.25,
                           'i_offset': 0.0,
                           'tau_m': 20.0,
                           'tau_refrac': 2.0,
                           'tau_syn_E': 5.0,
                           'tau_syn_I': 5.0,
                           'v_reset': -70.0,
                           'v_rest': -65.0,
                           'v_thresh': -50.0}
        n_neurons = 10
        if_curr_exp = IFCurrExpBase(
            n_neurons, 1000, 1.0, **cell_params_lif)
        self.assertEqual(if_curr_exp._model_name, "IF_curr_exp")
        self.assertEqual(len(if_curr_exp.get_parameters()), 10)
        self.assertEqual(if_curr_exp._v_thresh, cell_params_lif['v_thresh'])
        self.assertEqual(if_curr_exp._v_reset, cell_params_lif['v_reset'])
        self.assertEqual(if_curr_exp._v_rest, cell_params_lif['v_rest'])
        self.assertEqual(if_curr_exp._tau_m, cell_params_lif['tau_m'])
        self.assertEqual(if_curr_exp._tau_refrac,
                         cell_params_lif['tau_refrac'])

        self.assertEqual(if_curr_exp._tau_syn_I, cell_params_lif['tau_syn_I'])
        self.assertEqual(if_curr_exp._tau_syn_E, cell_params_lif['tau_syn_E'])
        self.assertEqual(if_curr_exp._i_offset, cell_params_lif['i_offset'])
        self.assertEqual(if_curr_exp._cm, cell_params_lif['cm'])

    @unittest.skip("empty test")
    def test_delay_vertex(self):
        pass

    @unittest.skip("empty test")
    def test_get_spikes(self):
        pass


if __name__ == "__main__":
    unittest.main()
