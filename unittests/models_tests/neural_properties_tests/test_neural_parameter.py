import unittest
from data_specification.enums.data_type import DataType
from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter


class TestingNeuronParameter(unittest.TestCase):
    def test_create_new_neuron_parameter_none_datatype(self):
        np = NeuronParameter(1, DataType.INT64)
        self.assertEqual(np.get_value(), 1)
        self.assertEqual(np.get_dataspec_datatype(), DataType.INT64)


if __name__ == '__main__':
    unittest.main()
