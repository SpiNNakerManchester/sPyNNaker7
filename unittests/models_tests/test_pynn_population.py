#!/usr/bin/env python
import os
import re
import struct
import tempfile
import unittest
import numpy
from pacman.model.graphs.machine import SimpleMachineVertex
from pacman.model.graphs.common import GraphMapper, Slice
from pacman.model.placements import Placements, Placement
from pacman.model.constraints.placer_constraints import ChipAndCoreConstraint
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spinn_front_end_common.utilities.globals_variables import get_simulator
from spinn_storage_handlers import BufferedBytearrayDataStorage
import spynnaker7.pyNN as pyNN

populations = list()
cell_params_lif = {'cm': 0.25,
                   'i_offset': 0.0,
                   'tau_m': 20.0,
                   'tau_refrac': 2.0,
                   'tau_syn_E': 5.0,
                   'tau_syn_I': 5.0,
                   'v_reset': -70.0,
                   'v_rest': -65.0,
                   'v_thresh': -50.0}
cell_params_izk = {
    'a': 0.02,
    'c': -65.0,
    'b': 0.2,
    'd': 2.0,
    'i_offset': 0,
    'u_init': -14.0,
    'v_init': -70.0,
    'tau_syn_E': 5.0,
    'tau_syn_I': 5.0}


class MockBufferManager(object):

    def __init__(self, data_to_return):
        self._data_to_return = data_to_return

    def get_data_for_vertex(self, placement, recording_region_id):
        return self._data_to_return[(placement, recording_region_id)]

    def stop(self):
        pass


class TestPyNNPopulation(unittest.TestCase):
    def setUp(self):
        pyNN.setup(timestep=1, min_delay=1, max_delay=10.0)

    def tearDown(self):
        pyNN.end()

    def test_create_if_curr_exp_population(self):
        pyNN.Population(1, pyNN.IF_curr_exp, cell_params_lif,
                        label="One population")

    def test_create_if_cond_exp_population(self):
        pyNN.Population(1, pyNN.IF_cond_exp, {}, label="One population")

    def test_create_izk_curr_exp_population(self):
        pyNN.Population(1, pyNN.extra_models.IZK_curr_exp,
                        cell_params_izk, label="One population")

    def test_create_if_curr_dual_exp_population(self):
        pyNN.Population(1, pyNN.extra_models.IF_curr_dual_exp, cell_params_lif,
                        label="One population")

    def test_create_if_curr_exp_population_zero(self):
        with self.assertRaises(ConfigurationException):
            pyNN.Population(0, pyNN.IF_curr_exp, cell_params_lif,
                            label="One population")

    def test_create_if_cond_exp_population_zero(self):
        with self.assertRaises(ConfigurationException):
            pyNN.Population(0, pyNN.IF_cond_exp, {}, label="One population")

    def test_create_izk_curr_exp_population_zero(self):
        with self.assertRaises(ConfigurationException):
            pyNN.Population(0, pyNN.extra_models.IZK_curr_exp,
                            cell_params_izk, label="One population")

    def test_create_if_curr_dual_exp_population_zero(self):
        with self.assertRaises(ConfigurationException):
            pyNN.Population(0, pyNN.extra_models.IF_curr_dual_exp,
                            cell_params_lif, label="One population")

    def test_population_size(self):
        pop0 = pyNN.Population(
            1, pyNN.IF_curr_exp, cell_params_lif, label="One population")
        pop1 = pyNN.Population(
            10, pyNN.IF_curr_exp, cell_params_lif, label="Two population")
        self.assertEqual(pop0._size, 1)
        self.assertEqual(pop1._size, 10)

    @unittest.skip("Not implemented")
    def test_get_spikes_from_virtual_spinnaker(self):
        self.assertEqual(True, False, "Test not implemented yet")

    def test_set_constraint_to_population(self):
        pop = pyNN.Population(10, pyNN.IF_curr_exp, cell_params_lif,
                              label="Constrained population")
        placer_constraint = ChipAndCoreConstraint(x=1, y=0)
        pop.set_constraint(placer_constraint)
        constraints = pop._get_vertex.constraints
        self.assertIn(placer_constraint, constraints)

    def test_t_set(self):
        pop = pyNN.Population(10, pyNN.IF_curr_exp, cell_params_lif,
                              label="Constrained population")
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        pop.tset("cm", data)
        cm = pop.get("cm")
        for index in range(0, len(data)):
            self.assertEqual(cm[index], data[index])

    def test_t_set_invalid(self):
        pop = pyNN.Population(10, pyNN.IF_curr_exp, cell_params_lif,
                              label="Constrained population")
        data = [0, 1, 2, 3, 4, 5, 6, 7]
        with self.assertRaises(ConfigurationException):
            pop.tset("cm", data)

    @unittest.skip("unittests/models_tests/test_pynn_population "
                   "test_get_default_parameters_of_if_curr_exp")
    def test_get_default_parameters_of_if_curr_exp(self):
        pop = pyNN.Population(10, pyNN.IF_curr_exp, cell_params_lif,
                              label="Constrained population")
        default_params = pop.default_parameters
        boxed_defaults = \
            {'tau_m': 20.0, 'cm': 1.0, 'v_rest': -65.0, 'v_reset': -65.0,
             'v_thresh': -50.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
             'tau_refrac': 0.1, 'i_offset': 0, 'v_init': -65.0}
        for param in default_params.keys():
            self.assertEqual(default_params[param], boxed_defaults[param])

    @unittest.skip("unittests/models_tests/test_pynn_population "
                   "test_get_default_parameters_of_if_"
                   "curr_exp_no_instaniation")
    def test_get_default_parameters_of_if_curr_exp_no_instaniation(self):
        default_params = pyNN.IF_curr_exp.default_parameters
        boxed_defaults = \
            {'tau_m': 20.0, 'cm': 1.0, 'v_rest': -65.0, 'v_reset': -65.0,
             'v_thresh': -50.0, 'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
             'tau_refrac': 0.1, 'i_offset': 0, 'v_init': -65.0}
        for param in default_params.keys():
            self.assertEqual(default_params[param], boxed_defaults[param])

    def test_spikes_per_second_setting_in_a_pop(self):
        pop = pyNN.Population(
            10, pyNN.IF_curr_exp, {'spikes_per_second': 3333},
            label="Constrained population")
        spikes_per_second = pop._get_vertex.spikes_per_second
        self.assertEqual(spikes_per_second, 3333)

    def test_spikes_per_second_not_set_in_a_pop(self):
        pop = pyNN.Population(
            10, pyNN.IF_curr_exp, cell_params_lif,
            label="Constrained population")
        spikes_per_second = pop._get_vertex.spikes_per_second
        self.assertEqual(spikes_per_second, 30)

    def test_ring_buffer_sigma_setting_in_a_pop(self):
        pop = pyNN.Population(
            10, pyNN.IF_curr_exp, {'ring_buffer_sigma': 3333},
            label="Constrained population")
        ring_buffer_sigma = pop._get_vertex.ring_buffer_sigma
        self.assertEqual(ring_buffer_sigma, 3333)

    def test_ring_buffer_sigma_not_set_in_a_pop(self):
        pop = pyNN.Population(
            10, pyNN.IF_curr_exp, cell_params_lif,
            label="Constrained population")
        ring_buffer_sigma = pop._get_vertex.ring_buffer_sigma
        self.assertEqual(ring_buffer_sigma, 5.0)

    def test_print(self):
        pop = pyNN.Population(
            2, pyNN.IF_curr_exp, cell_params_lif, label="Test")
        pop.record()
        pop.record_v()
        pop.record_gsyn()
        machine_vertex = SimpleMachineVertex(resources=None)
        graph_mapper = GraphMapper()
        graph_mapper.add_vertex_mapping(
            machine_vertex, Slice(0, 1), pop._vertex)
        placements = Placements()
        placement = Placement(machine_vertex, 0, 0, 0)
        placements.add_placement(placement)

        spike_data = BufferedBytearrayDataStorage()
        spike_data.write(bytearray(struct.pack("<II", 0, 0x3)))
        spike_data.write(bytearray(struct.pack("<II", 1, 0x1)))
        spike_data.write(bytearray(struct.pack("<II", 2, 0x2)))

        v_data = BufferedBytearrayDataStorage()
        sixteen = 16 * 32768
        thirtytwo = 32 * 32768
        v_data.write(bytearray(struct.pack("<III", 0, sixteen, sixteen)))
        v_data.write(bytearray(struct.pack("<III", 1, thirtytwo, sixteen)))
        v_data.write(bytearray(struct.pack("<III", 2, sixteen, thirtytwo)))

        gsyn_ex_data = BufferedBytearrayDataStorage()
        gsyn_ex_data.write(bytearray(struct.pack(
            "<III", 0, sixteen, sixteen)))
        gsyn_ex_data.write(bytearray(struct.pack(
            "<III", 1, thirtytwo, sixteen)))
        gsyn_ex_data.write(bytearray(struct.pack(
            "<III", 2, sixteen, thirtytwo)))
        gsyn_in_data = BufferedBytearrayDataStorage()
        gsyn_in_data.write(bytearray(struct.pack("<III", 0, 0, 0)))
        gsyn_in_data.write(bytearray(struct.pack("<III", 1, 0, 0)))
        gsyn_in_data.write(bytearray(struct.pack("<III", 2, 0, 0)))

        recorded_data = {
            (placement, 0): (spike_data, False),
            (placement, 1): (v_data, False),
            (placement, 2): (gsyn_ex_data, False),
            (placement, 3): (gsyn_in_data, False)
        }
        sim = get_simulator()
        sim._has_ran = True
        sim._buffer_manager = MockBufferManager(recorded_data)
        sim._graph_mapper = graph_mapper
        sim._placements = placements
        sim._no_machine_time_steps = 3
        temp_spikes_file_name = tempfile.mktemp(".dat")
        temp_v_file_name = tempfile.mktemp(".dat")
        temp_gsyn_file_name = tempfile.mktemp(".dat")
        pop.printSpikes(temp_spikes_file_name)
        pop.print_v(temp_v_file_name)
        pop.print_gsyn(temp_gsyn_file_name)

        spikes_metadata = dict()
        with open(temp_spikes_file_name, "r") as spikes_file:
            for line in spikes_file:
                match = re.match("# (.*) = (.*)", line)
                if match:
                    spikes_metadata[match.group(1)] = match.group(2)
        spike_data = numpy.loadtxt(temp_spikes_file_name)
        assert spikes_metadata["variable"] == "spikes"
        assert int(spikes_metadata["first_id"]) == 0
        assert int(spikes_metadata["last_id"]) == 1
        assert int(spikes_metadata["first_index"]) == 0
        assert int(spikes_metadata["last_index"]) == 2
        assert int(spikes_metadata["n"]) == len(spike_data)
        assert int(spikes_metadata["size"]) == 2
        assert float(spikes_metadata["dt"]) == 1.0
        assert len(spike_data) == 4
        assert all([len(spike_data[i]) == 2 for i in range(len(spike_data))])
        assert numpy.array_equal(spike_data, [[0, 0], [1, 0], [0, 1], [2, 1]])

        v_metadata = dict()
        with open(temp_v_file_name, "r") as v_file:
            for line in v_file:
                match = re.match("# (.*) = (.*)", line)
                if match:
                    v_metadata[match.group(1)] = match.group(2)
        v_data = numpy.loadtxt(temp_v_file_name)
        assert v_metadata["variable"] == "v"
        assert int(v_metadata["first_id"]) == 0
        assert int(v_metadata["last_id"]) == 1
        assert int(v_metadata["first_index"]) == 0
        assert int(v_metadata["last_index"]) == 2
        assert int(v_metadata["n"]) == len(v_data)
        assert int(v_metadata["size"]) == 2
        assert float(v_metadata["dt"]) == 1.0
        assert len(v_data) == 6
        assert all([len(v_data[i]) == 2 for i in range(len(v_data))])
        assert numpy.array_equal(
            v_data, [[16, 0], [32, 0], [16, 0], [16, 1], [16, 1], [32, 1]])

        gsyn_metadata = dict()
        with open(temp_gsyn_file_name, "r") as gsyn_file:
            for line in gsyn_file:
                match = re.match("# (.*) = (.*)", line)
                if match:
                    gsyn_metadata[match.group(1)] = match.group(2)
        gsyn_data = numpy.loadtxt(temp_gsyn_file_name)
        assert gsyn_metadata["variable"] == "gsyn"
        assert int(gsyn_metadata["first_id"]) == 0
        assert int(gsyn_metadata["last_id"]) == 1
        assert int(gsyn_metadata["first_index"]) == 0
        assert int(gsyn_metadata["last_index"]) == 2
        assert int(gsyn_metadata["n"]) == len(gsyn_data)
        assert int(gsyn_metadata["size"]) == 2
        assert float(gsyn_metadata["dt"]) == 1.0
        assert len(gsyn_data) == 6
        assert all([len(gsyn_data[i]) == 3 for i in range(len(gsyn_data))])
        assert numpy.array_equal(
            gsyn_data, [[16, 0, 0], [32, 0, 0], [16, 0, 0],
                        [16, 0, 1], [16, 0, 1], [32, 0, 1]])

        os.unlink(temp_spikes_file_name)
        os.unlink(temp_v_file_name)
        os.unlink(temp_gsyn_file_name)


if __name__ == "__main__":
    unittest.main()
