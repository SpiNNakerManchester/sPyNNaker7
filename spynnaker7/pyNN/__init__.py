import inspect as __inspect
import logging as __logging
import numpy as __numpy
import os as __os
from spinn_utilities.log import FormatAdapter
from spinn_utilities.overrides import overrides

import spynnaker7
from pyNN.random import NumpyRNG, RandomDistribution as _PynnRandomDistribution
from pyNN.space import \
    distance as _pynn_distance, Space, Line, Grid2D, Grid3D, Cuboid, Sphere, \
    RandomStructure
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spinn_front_end_common.utilities import globals_variables

from spynnaker.pyNN.models.neural_projections.delay_afferent_application_edge \
    import DelayAfferentApplicationEdge
from spynnaker.pyNN.models.neural_projections.projection_application_edge \
    import ProjectionApplicationEdge
from spynnaker.pyNN.models.neuron.builds.if_cond_exp_base \
    import IFCondExpBase as IF_cond_exp
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_base \
    import IFCurrExpBase as IF_curr_exp
from spynnaker.pyNN.models.neuron.builds.if_curr_alpha \
    import IFCurrAlpha as IF_curr_alpha
from spynnaker.pyNN.models.neuron.synapse_dynamics.pynn_synapse_dynamics \
    import PyNNSynapseDynamics as SynapseDynamics
from spynnaker.pyNN.models.neuron.synapse_dynamics.synapse_dynamics_stdp \
    import SynapseDynamicsSTDP as STDPMechanism
from spynnaker.pyNN.models.neuron.synapse_dynamics\
    .synapse_dynamics_structural \
    import SynapseDynamicsStructural as StructuralMechanism
from spynnaker.pyNN.models.spike_source.spike_source_array \
    import SpikeSourceArray
from spynnaker.pyNN.models.spike_source.spike_source_from_file \
    import SpikeSourceFromFile
from spynnaker.pyNN.models.spike_source.spike_source_poisson \
    import SpikeSourcePoisson
from spynnaker.pyNN.models.spike_source.spike_source_poisson_variable \
    import SpikeSourcePoissonVariable
from spynnaker.pyNN.models.utility_models.delay_extension_vertex \
    import DelayExtensionVertex
from spynnaker.pyNN.utilities import utility_calls

from spynnaker7.pyNN.models.connectors.all_to_all_connector \
    import AllToAllConnector
from spynnaker7.pyNN.models.connectors. \
    distance_dependent_probability_connector import \
    DistanceDependentProbabilityConnector
from spynnaker7.pyNN.models.connectors.fixed_number_post_connector \
    import FixedNumberPostConnector
from spynnaker7.pyNN.models.connectors.fixed_number_pre_connector \
    import FixedNumberPreConnector
from spynnaker7.pyNN.models.connectors.fixed_probability_connector \
    import FixedProbabilityConnector
from spynnaker7.pyNN.models.connectors.from_file_connector \
    import FromFileConnector
from spynnaker7.pyNN.models.connectors.from_list_connector import \
    FromListConnector
from spynnaker7.pyNN.models.connectors.multapse_connector \
    import MultapseConnector
from spynnaker7.pyNN.models.connectors.one_to_one_connector \
    import OneToOneConnector
from spynnaker7.pyNN.models.plasticity_components.timing_dependence \
    .timing_dependence_spike_pair \
    import TimingDependenceSpikePair as SpikePairRule
from spynnaker7.pyNN.models.plasticity_components.weight_dependence.\
    weight_dependence_additive \
    import WeightDependenceAdditive as AdditiveWeightDependence
from spynnaker7.pyNN.models.plasticity_components.weight_dependence \
    .weight_dependence_multiplicative \
    import WeightDependenceMultiplicative as MultiplicativeWeightDependence

from spynnaker7.pyNN import external_devices
from spynnaker7.pyNN import extra_models

from spynnaker7.pyNN.spinnaker import Spinnaker as __Spinnaker
from spynnaker7._version import __version__  # NOQA
from spynnaker7._version import __version_name__  # NOQA
from spynnaker7._version import __version_month__  # NOQA
from spynnaker7._version import __version_year__  # NOQA

# traditional logger
logger = FormatAdapter(__logging.getLogger(__name__))

# List of binary search paths
_binary_search_paths = []

__all__ = [
    # Ugly, but tests expect it
    'utility_calls',
    # Implementations of the neuroscience models
    'IF_cond_exp', 'IF_curr_exp', "IF_curr_alpha",
    'DelayAfferentApplicationEdge', 'DelayExtensionVertex',
    'ProjectionApplicationEdge', 'SpikeSourcePoisson',
    'SpikeSourcePoissonVariable', 'SpikeSourceArray',
    'SpikeSourceFromFile', 'AllToAllConnector', 'FixedNumberPreConnector',
    'FixedProbabilityConnector', 'FromListConnector', 'FromFileConnector',
    'MultapseConnector', 'OneToOneConnector', 'FixedNumberPostConnector',
    'DistanceDependentProbabilityConnector', 'SynapseDynamics',
    'STDPMechanism', 'StructuralMechanism', 'AdditiveWeightDependence',
    'SpikePairRule', 'MultiplicativeWeightDependence',
    # Stuff from pyNN.random
    'NumpyRNG', 'RandomDistribution',
    # Stuff from pyNN.space
    'distance', 'Space', 'Line', 'Grid2D', 'Grid3D', 'Cuboid', 'Sphere',
    'RandomStructure',
    # External devices and extra models
    'external_devices', 'extra_models',
    # Stuff that we define
    'end', 'setup', 'run', 'get_spynnaker', 'get_projections_data',
    'num_processes', 'rank', 'reset', 'set_number_of_neurons_per_core',
    'Population', 'Projection',
    'NativeRNG', 'get_current_time', 'create', 'connect', 'get_time_step',
    'get_min_delay', 'get_max_delay', 'set', 'initialize', 'record',
    'record_v', 'record_gsyn', 'get_machine']


# Patch the bugs in the PyNN documentation... Ugh!
class RandomDistribution(_PynnRandomDistribution):
    """ Class which defines a ``next(n)`` method which returns an array of\
        :emphasis:`n` random numbers from a given distribution.
    """

    @overrides(_PynnRandomDistribution.__init__, extend_doc=False)
    def __init__(self, distribution='uniform', parameters=None, rng=None,
                 boundaries=None, constrain="clip"):
        """
        :param rng: If present, should be a NumpyRNG or GSLRNG object.
        :param distribution: should be the name of a method supported by the\
            underlying random number generator object.
        :param parameters: should be a list or tuple containing the arguments\
            expected by the underlying method in the correct order. Named\
            arguments are not yet supported.
        :param boundaries: a tuple (min, max) used to specify explicitly, for\
            distributions like Gaussian, Gamma or others, hard boundaries for\
            the parameters. If parameters are drawn outside those boundaries,\
            the policy applied will depend on the constrain parameter.
        :param constrain: controls the policy for weights out of the specified\
            boundaries. If "``clip``", random numbers are clipped to the\
            boundaries. If "``redraw``", random numbers are drawn till they\
            fall within the boundaries.

        .. note::
            Note that NumpyRNG and GSLRNG distributions may not have the same\
            names, e.g., "``normal``" for NumpyRNG and "``gaussian``" for\
            GSLRNG, and the arguments may also differ.
        """
        parameters = [] if parameters is None else parameters
        super(RandomDistribution, self).__init__(
            distribution, parameters, rng, boundaries, constrain)

    @overrides(_PynnRandomDistribution.next, extend_doc=False)
    def next(self, n=1, mask_local=None):
        """ Return *n* random numbers from the distribution.

        :param n: The number of random numbers to return.
        :param mask_local: Leave set to ``None`` (the default).
        :return: sequence of random numbers, or a random number if *n* is 1.
        """
        return super(RandomDistribution, self).next(n, mask_local)


# Patch the bugs in the PyNN documentation... Ugh!
def distance(src, tgt, mask=None, scale_factor=1.0, offset=0.0,
             periodic_boundaries=None):
    """ Return the Euclidian distance between two cells.

    :param mask: allows only certain dimensions to be considered, e.g.:
        * to ignore the z-dimension, use ``mask=array([0,1])``
        * to ignore y, ``mask=array([0,2])``
        * to just consider z-distance, ``mask=array([2])``
    :param scale_factor: allows for different units in the pre- and post-\
        position (the post-synaptic position is multiplied by this quantity).
    """
    return _pynn_distance(
        src, tgt, mask, scale_factor, offset, periodic_boundaries)


def get_projections_data(projection_data):
    return globals_variables.get_simulator().get_projections_data(
        projection_data)


def end():
    """ Do any necessary cleaning up before exiting.

    Unregisters the controller,\
    prints any data recorded using the low-level API
    """
    globals_variables.get_simulator().stop()
    # _spinnaker = None


def get_spynnaker():
    """ Helper method for other plugins to add stuff to the graph

    :return: The current spinnaker API, or None if before setup or after end.
    """
    return globals_variables.get_simulator()


def num_processes():
    """ Return the number of MPI processes\
        (not used for SpiNNaker, always returns 1)
    """
    return 1


def rank():
    """ Return the MPI rank of the current node. (not used for SpiNNaker,\
        always returns 0 - as this is the minimum rank suggesting the front\
        node)
    """
    return 0


def reset():
    """ Reset the time to zero, and start the clock.
    """
    globals_variables.get_not_running_simulator().reset()


def run(run_time=None):
    """ Run the simulation for run_time ms.

    :param run_time: simulation length (in ms)
    """
    globals_variables.get_simulator().run(run_time)
    return None


def setup(timestep=0.1, min_delay=None, max_delay=None, machine=None,
          database_socket_addresses=None, n_chips_required=None,
          **extra_params):
    """ Should be called at the very beginning of a script.\
        extra_params contains any keyword arguments that are required by a\
        given simulator but not by others.

    :param machine: A SpiNNaker machine used to run the simulation.
    :param timestep: The timestep in milliseconds.\
       Value will be rounded up to whole microseconds.\
       Set to None to use the value from the configuration file
    :param min_delay: the minimum number of time steps supported for delays
    :param max_delay: the maximum number of time steps supported for delays
    :param machine: The machine ip address
    :param database_socket_addresses: the set of sockets needed to be listened\
        to for database notification protocol
    :param n_chips_required: The number of chips required for the simulation
    :param extra_params: random other crap
    :rtype: float or None
    """
    logger.info(
        "sPyNNaker (c) {} APT Group, University of Manchester",
        __version_year__)
    parent_dir = __os.path.split(__os.path.split(spynnaker7.__file__)[0])[0]
    logger.info(
        "Release version {}({}) - {} {}. Installed in folder {}",
        __version__, __version_name__, __version_month__, __version_year__,
        parent_dir)

    if extra_params:
        logger.warning("Extra params {} have been applied to the setup "
                       "command which we do not consider", extra_params)
    __Spinnaker(
        host_name=machine, timestep=timestep, min_delay=min_delay,
        max_delay=max_delay,
        database_socket_addresses=database_socket_addresses,
        n_chips_required=n_chips_required)

    # the PyNN API expects the MPI rank to be returned
    return rank()


def set_number_of_neurons_per_core(neuron_type, max_permitted):
    """ Sets a ceiling on the number of neurons of a given type that can be\
        placed on a single core.

    :param neuron_type: the neuron type that will have its max atoms set
    :param max_permitted: The max amount of atoms to be set
    :type neuron_type: The string representation of the neuron type
    :type max_permitted: int
    :rtype: None
    """
    if not __inspect.isclass(neuron_type):
        if neuron_type not in globals():
            raise Exception("Unknown Vertex Type {}".format(neuron_type))
        neuron_type = globals()[neuron_type]

    simulator = globals_variables.get_not_running_simulator()
    simulator.set_number_of_neurons_per_core(neuron_type, max_permitted)


# noinspection PyPep8Naming
def Population(size, cellclass, cellparams, structure=None, label=None):
    """ Builds a new population object.

    :param size: n neurons
    :param cellclass: the neuron class that needs to be created
    :param cellparams: the parameters to put into the neuron model
    :param structure: a structure that describes the arrangement of the\
        neurons of the population in space
    :param label: the human readable label
    :return: a new population object
    """

    globals_variables.get_simulator().verify_not_running()
    return globals_variables.get_not_running_simulator().create_population(
        size, cellclass, cellparams, structure, label)


# noinspection PyPep8Naming
def Projection(presynaptic_population, postsynaptic_population,
               connector, source=None, target='excitatory',
               synapse_dynamics=None, label=None, rng=None):
    """ Builds a new projection object.

    :param presynaptic_population: the source pop
    :param postsynaptic_population: the destination pop
    :param connector: the connector describing connectivity
    :param source: string specifying which attribute of the presynaptic cell\
        signals action potentials, or None for the default
    :param target: type of synapse, excitatory or inhibitory for example.
    :param synapse_dynamics: plasticity
    :param label: human readable label
    :param rng: random number generator if needed
    :return: a new Projection object
    """
    globals_variables.get_simulator().verify_not_running()
    return globals_variables.get_not_running_simulator().create_projection(
        presynaptic_population, postsynaptic_population, connector, source,
        target, synapse_dynamics, label, rng)


def NativeRNG(seed_value):
    """ Fixes the random number generator's seed

    :param seed_value:
    :return:
    """
    __numpy.random.seed(seed_value)


def get_current_time():
    """ Returns the machine time step defined in setup

    :return: the runtime currently
    """
    return globals_variables.get_simulator().get_current_time()


# =============================================================================
#  Low-level API for creating, connecting and recording from individual neurons
# =============================================================================

def create(cellclass, cellparams=None, n=1):
    """ Create *n* cells all of the same type.

    If *n* > 1, return a list of cell IDs/references.
    If *n* == 1, return just the single ID.
    """
    if cellparams is None:
        cellparams = {}
    return Population(n, cellclass, cellparams)


def connect(source, target, weight=0.0, delay=None, synapse_type="excitatory",
            p=1, rng=None):
    """ Connect a source of spikes to a synaptic target.

    ``source`` and ``target`` can both be individual cells or lists of cells,\
    in which case all possible connections are made with probability ``p``,\
    using either the random number generator supplied, or the default RNG\
    otherwise. Weights should be in nA or uS.
    """
    connector = FixedProbabilityConnector(
        p_connect=p, weights=weight, delays=delay)
    return Projection(source, target, connector, target=synapse_type, rng=rng)


def get_time_step():
    """ The timestep requested

    :return:
    """
    return globals_variables.get_simulator().machine_time_step


def get_min_delay():
    """ The minimum allowed synaptic delay.

    :return:
    """
    return globals_variables.get_simulator().min_delay


def get_max_delay():
    """ The maximum allowed synaptic delay.

    :return:
    """
    return globals_variables.get_simulator().max_delay


def set(cells, param, val=None):  # @ReservedAssignment
    """ Set one or more parameters of an individual cell or list of cells.

    ``param`` can be a dict, in which case ``val`` should not be supplied, or\
    a string giving the parameter name, in which case ``val`` is the\
    parameter value.
    """
    # pylint: disable=redefined-builtin
    assert isinstance(cells, Population)
    cells.set(param, val)


def initialize(cells, variable, value):
    cells.initialize(variable, value)


def record(source, filename):
    """ Record spikes to a file. source should be a Population.
    """
    source.record(to_file=filename)


def record_v(source, filename):
    """ Record spikes to a file. source should be a Population.
    """
    source.record_v(to_file=filename)


def record_gsyn(source, filename):
    """ Record spikes to a file. source should be a Population.
    """
    source.record_gsyn(to_file=filename)


def get_machine():
    """ Get the spinnaker machine in use
    """
    if not globals_variables.has_simulator():
        raise ConfigurationException(
            "You currently have not ran setup, please do so before calling "
            "get_machine")
    return globals_variables.get_simulator().machine
