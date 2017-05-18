import os
import sys
import unittest

from spynnaker7.pyNN.spinnaker import Spinnaker as Spinnaker
from spynnaker.pyNN.models.neuron.builds.if_cond_exp_base \
    import IFCondExpBase as IF_cond_exp
from spynnaker.pyNN.models.neuron.builds.if_curr_dual_exp_base \
    import IFCurrDualExpBase as IF_curr_dual_exp
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_base \
    import IFCurrExpBase as IF_curr_exp
from spynnaker.pyNN.models.neuron.builds.izk_cond_exp_base \
    import IzkCondExpBase as IZK_cond_exp
from spynnaker.pyNN.models.neuron.builds.izk_curr_exp_base \
    import IzkCurrExpBase as IZK_curr_exp
from spynnaker.pyNN.models.spike_source.spike_source_array \
    import SpikeSourceArray
from spynnaker.pyNN.models.spike_source.spike_source_poisson \
    import SpikeSourcePoisson


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        class_file = sys.modules[self.__module__].__file__
        path = os.path.dirname(os.path.abspath(class_file))
        os.chdir(path)
        # Some tests changes this so change it back here!
        IF_cond_exp.set_model_max_atoms_per_core()
        IF_curr_dual_exp.set_model_max_atoms_per_core()
        IF_curr_exp.set_model_max_atoms_per_core()
        IZK_cond_exp.set_model_max_atoms_per_core()
        IZK_curr_exp.set_model_max_atoms_per_core()
        SpikeSourceArray.set_model_max_atoms_per_core()
        SpikeSourcePoisson.set_model_max_atoms_per_core()

    def assert_logs_error(self, log_records, sub_message):
        for record in log_records:
            print record
            if record.levelname == 'ERROR':
                if sub_message in record.msg:
                    return
        msg = "\"{}\" not found in any ERROR logs".format(sub_message)
        raise self.failureException(msg)
