import os
import sys
import unittest

import spynnaker7.pyNN.utilities.conf as conf
from spynnaker7.pyNN.spinnaker import Spinnaker as Spinnaker
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_base \
    import IFCurrExpBase as IF_curr_exp


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        class_file = sys.modules[self.__module__].__file__
        path = os.path.dirname(os.path.abspath(class_file))
        os.chdir(path)
        config = conf.load_config()
        Spinnaker._set_config(config)
        # Some tests changes this so change it back here!
        IF_curr_exp.set_model_max_atoms_per_core()

    def assert_logs_error(self, log_records, sub_message):
        for record in log_records:
            print record
            if record.levelname == 'ERROR':
                if sub_message in record.msg:
                    return
        msg = "\"{}\" not found in any ERROR logs".format(sub_message)
        raise self.failureException(msg)
