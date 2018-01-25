from spynnaker.pyNN.models.pynn_population_common import PyNNPopulationCommon
from spynnaker.pyNN.models.recording_common import RecordingCommon
from spynnaker.pyNN.utilities import utility_calls
from spynnaker.pyNN.utilities.constants import \
    SPIKES, MEMBRANE_POTENTIAL, GSYN_INHIB, GSYN_EXCIT
from spinn_front_end_common.utilities.exceptions import ConfigurationException

from pyNN import descriptions

import logging

logger = logging.getLogger(__name__)


class Population(PyNNPopulationCommon, RecordingCommon):
    """ A collection neuron of the same types. It encapsulates a type of\
        vertex used with Spiking Neural Networks, comprising n cells (atoms)\
        of the same model type.

    :param int size:
        size (number of cells) of the Population.
    :param cellclass:
        specifies the neural model to use for the Population
    :param dict cellparams:
        a dictionary containing model specific parameters and values
    :param structure:
        a spatial structure
    :param string label:
        a label identifying the Population
    """

    def __init__(self, size, cellclass, cellparams, spinnaker, label,
                 structure=None):

        size = self._roundsize(size, label)

        internal_cellparams = dict(cellparams)

        # set spinnaker targeted parameters
        model_label = None
        if 'label' in internal_cellparams:
            model_label = internal_cellparams['label']
        internal_cellparams['label'] = self.create_label(model_label, label)
        internal_cellparams['n_neurons'] = size

        # create population vertex.
        vertex = cellclass(**internal_cellparams)

        PyNNPopulationCommon.__init__(
            self, spinnaker_control=spinnaker, size=size, vertex=vertex,
            initial_values=None, structure=structure)
        RecordingCommon.__init__(self, self)

    @property
    def default_parameters(self):
        """ The default parameters of the vertex from this population
        """
        return self._vertex.default_parameters

    def describe(self, template='population_default.txt', engine='default'):
        """ Returns a human-readable description of the population.

        The output may be customised by specifying a different template
        together with an associated template engine (see ``pyNN.descriptions``)

        If template is None, then a dictionary containing the template context
        will be returned.
        """

        vertex_context = self._vertex.describe()

        context = {
            "label": self.label,
            "celltype": descriptions.render(
                engine, 'modeltype_default.txt', vertex_context),
            "structure": None,
            "size": self.size,
            "size_local": self.size,
            "first_id": self._first_id,
            "last_id": self._last_id,
        }
        if self.size > 0:
            context.update({
                "local_first_id": None,
                "cell_parameters": {}})

        if self._structure:
            context["structure"] = self._structure.describe(template=None)
        return descriptions.render(engine, template, context)

    # noinspection PyPep8Naming
    def getSpikes(self, compatible_output=True, gather=True):
        """
        Return a 2-column numpy array containing cell ids and spike times for\
        recorded cells.
        """
        self._compatible_output_and_gather_warnings(compatible_output, gather)
        return self._get_spikes()

    def get_spike_counts(self, gather=True):
        """ Return the number of spikes for each neuron.
        """
        spikes = self.getSpikes(True, gather)
        return PyNNPopulationCommon.get_spike_counts(self, spikes, gather)

    # noinspection PyUnusedLocal
    def get_gsyn(self, gather=True, compatible_output=True):
        """
        Return a 3-column numpy array containing cell ids, time and synaptic\
        conductances for recorded cells.

        :param gather: not used - inserted to match PyNN specs
        :type gather: bool
        :param compatible_output: not used - inserted to match PyNN specs
        :type compatible_output: bool
        """

        self._compatible_output_and_gather_warnings(compatible_output, gather)
        (exc_data, exc_ids, exc_sampling_interval) = \
            self._get_recorded_matrix("gsyn_exc")
        (inh_data, inh_ids, inh_sampling_interval) = \
            self._get_recorded_matrix("gsyn_inh")
        # TODO this needs fixing for to check ids and interval are the same
        return self.pynn7_format(
            exc_data, exc_ids, exc_sampling_interval, inh_data)

    # noinspection PyUnusedLocal
    def get_v(self, gather=True, compatible_output=True):
        """
        Return a 3-column numpy array containing cell ids, time, and V_m for\
        recorded cells.

        :param gather: not used - inserted to match PyNN specs
        :type gather: bool
        :param compatible_output: not used - inserted to match PyNN specs
        :type compatible_output: bool
        """
        self._compatible_output_and_gather_warnings(compatible_output, gather)
        return self._get_recorded_pynn7(MEMBRANE_POTENTIAL)

    @staticmethod
    def _compatible_output_and_gather_warnings(compatible_output, gather):
        """ checks the values for compatible out and gather warnings

        :param compatible_output: if compatible with pynn
        :param gather: if gathering from pynn
        :return: None
        """
        if not gather:
            logger.warn(
                "Spynnaker 0.7 only supports gather = True, will  execute "
                "as if gather was true anyhow")

        if not compatible_output:
            logger.warn(
                "Spynnaker 0.7 only supports compatible_output = True, will"
                " execute as if compatible_output was false anyhow")

    @staticmethod
    def is_local(cell_id):
        """ Determine whether the cell with the given ID exists on the local \
            MPI node.

        :param cell_id:
        """

        # Doesn't really mean anything on SpiNNaker
        return True

    # noinspection PyPep8Naming
    def meanSpikeCount(self, gather=True):
        """ The mean number of spikes per neuron

        :param gather: gather has no meaning in spinnaker, always set to true
        :return: an array which contains the average spike rate per neuron
        """
        return self.mean_spike_count(gather)

    def mean_spike_count(self, gather=True):
        """ The mean number of spikes per neuron
        """
        spike_counts = self.get_spike_counts(gather)
        total_spikes = sum(spike_counts.values())
        return total_spikes / self._size

    def nearest(self, position):
        """ Return the neuron closest to the specified position
        """
        # doesn't always work correctly if a position is equidistant between
        # two neurons, i.e. 0.5 should be rounded up, but it isn't always.
        # also doesn't take account of periodic boundary conditions

        # TODO: Enable when __getitem__ is enabled
        # pos = numpy.array([position] * self.positions.shape[1]).transpose()
        # dist_arr = (self.positions - pos) ** 2
        # distances = dist_arr.sum(axis=0)
        # nearest = distances.argmin()
        # return self[nearest]

        raise NotImplementedError

    # noinspection PyPep8Naming
    def randomInit(self, distribution):
        """ Set initial membrane potentials for all the cells in the\
            population to random values.

        :param `pyNN.random.RandomDistribution` distribution:\
            the distribution used to draw random values.

        """
        self.initialize('v', distribution)
        self._change_requires_mapping = True

    def record(self, to_file=None):
        """ Record spikes from all cells in the Population.

        :param to_file: file to write the spike data to
        """

        self._record(SPIKES, sampling_interval=1, to_file=to_file)

        # state that something has changed in the population,
        self._change_requires_mapping = True

    def record_gsyn(self, to_file=None):
        """ Record the synaptic conductance for all cells in the Population.

        :param to_file: the file to write the recorded gsyn to.
        """

        # have to set each to record and set the file at that point, otherwise
        # itll not work due to pynn bug
        self._record(GSYN_EXCIT, sampling_interval=1, to_file=to_file)
        self.file = to_file
        self._record(GSYN_INHIB, sampling_interval=1, to_file=to_file)
        self.file = to_file

        # state that something has changed in the population,
        self._change_requires_mapping = True

    def record_v(self, to_file=None):
        """ Record the membrane potential for all cells in the Population.

        :param to_file: the file to write the recorded v to.
        """

        self._record('v', sampling_interval=1, to_file=to_file)
        self.file = to_file

        # state that something has changed in the population,
        self._change_requires_mapping = True

    @property
    def positions(self):
        """ Return the position array for structured populations.
        """
        if self._positions is None:
            if self._structure is None:
                raise ValueError("attempted to retrieve positions "
                                 "for an unstructured population")
            self._positions = self._structure.generate_positions(
                self._vertex.n_atoms)
        return self._positions

    @positions.setter
    def positions(self, positions):
        """ Sets all the positions in the population.
        """
        self._positions = positions

        # state that something has changed in the population,
        self._change_requires_mapping = True

    def _print_headers(self, file_to_write, variable, n_data_points):
        time_step = (
                self._spinnaker_control.machine_time_step * 1.0) / 1000.0
        file_to_write.write("# variable = {}\n".format(variable))
        file_to_write.write("# first_index = 0\n")
        file_to_write.write("# last_index = {}\n".format(self._vertex.n_atoms))
        file_to_write.write("# first_id = {}\n".format(self._first_id))
        file_to_write.write("# last_id = {}\n".format(self._last_id))
        file_to_write.write("# n = {}\n".format(n_data_points))
        file_to_write.write("# size = {}\n".format(self._vertex.n_atoms))
        file_to_write.write("# dt = {}\n".format(time_step))

    # noinspection PyPep8Naming
    def printSpikes(self, filename, gather=True):
        """ Write spike time information from the population to a given file.

        :param filename: the absolute file path for where the spikes are to\
                    be printed in
        :param gather: Supported from the PyNN language, but ignored here
        """
        if not gather:
            logger.warn("Spynnaker only supports gather = true, will execute"
                        " as if gather was true anyhow")
        spikes = self._get_spikes()
        if spikes is not None:
            utility_calls.check_directory_exists_and_create_if_not(filename)
            spike_file = open(filename, "w")
            self._print_headers(spike_file, SPIKES, spikes.shape[0])
            for (neuronId, time) in spikes:
                spike_file.write("{}\t{}\n".format(time, neuronId))
            spike_file.close()

    def print_gsyn(self, filename, gather=True):
        """ Write conductance information from the population to a given file.

        :param filename: the absolute file path for where the gsyn are to be\
                    printed in
        :param gather: Supported from the PyNN language, but ignored here
        """
        gsyn = self.get_gsyn()

        utility_calls.check_directory_exists_and_create_if_not(filename)
        file_handle = open(filename, "w")
        self._print_headers(file_handle, "gsyn", gsyn.shape[0])
        for (neuronId, _, value_e, value_i) in gsyn:
            file_handle.write("{}\t{}\t{}\n".format(
                value_e, value_i, neuronId))
        file_handle.close()

    def print_v(self, filename, gather=True):
        """ Write membrane potential information from the population to a\
            given file.

        :param filename: the absolute file path for where the voltage are to\
                     be printed in
        :param gather: Supported from the PyNN language, but ignored here
        """
        v = self._get_recorded_pynn7(MEMBRANE_POTENTIAL)
        utility_calls.check_directory_exists_and_create_if_not(filename)
        file_handle = open(filename, "w")
        self._print_headers(file_handle, MEMBRANE_POTENTIAL, v.shape[0])
        for (neuronId, _, value) in v:
            file_handle.write("{}\t{}\n".format(value, neuronId))
        file_handle.close()

    def rset(self, parametername, rand_distr):
        """ 'Random' set. Set the value of parametername to a value taken\
             from rand_distr, which should be a RandomDistribution object.

        :param parametername: the parameter to set
        :param rand_distr: the random distribution object to set the parameter\
                     to
        """
        self.set(parametername, rand_distr)

    def sample(self, n, rng=None):
        """ Return a random selection of neurons from a population in the form\
            of a population view

        :param n: the number of neurons to sample
        :param rng: the random number generator to use.
        """

        # TODO: Need PopulationView support
        raise NotImplementedError

    def save_positions(self, file):  # @ReservedAssignment
        """ Save positions to file.

            :param file: the file to write the positions to.
        """
        file_handle = open(file, "w")
        file_handle.write(self.positions)
        file_handle.close()

    @property
    def structure(self):
        """ Return the structure for the population.
        """
        return self._structure

    def tset(self, parametername, value_array):
        """ 'Topographic' set. Set the value of parametername to the values in\
            value_array, which must have the same dimensions as the Population.

        :param parametername: the name of the parameter
        :param value_array: the array of values which must have the correct\
                number of elements.
        """
        if len(value_array) != self._vertex.n_atoms:
            raise ConfigurationException(
                "To use tset, you must have a array of values which matches "
                "the size of the population. Please change this and try "
                "again, or alternatively, use set()")
        self.set(parametername, value_array)

    def _end(self):
        """ Do final steps at the end of the simulation
        """
        if self._record_spike_file is not None:
            self.printSpikes(self._record_spike_file)
        if self._record_v_file is not None:
            self.print_v(self._record_v_file)
        if self._record_gsyn_file is not None:
            self.print_gsyn(self._record_gsyn_file)
