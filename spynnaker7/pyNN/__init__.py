import inspect

from spynnaker.pyNN.utilities.failed_state import FailedState
from ._version import __version__, __version_name__, __version_month__, \
    __version_year__

# main entrance
from spynnaker7.pyNN.spinnaker import Spinnaker

# pynn centric classes
from spynnaker.pyNN.spinnaker_common import executable_finder
from spynnaker.pyNN.utilities import globals_variables

# notification protocol classes (stored in front end common)
from spinn_front_end_common.utilities.notification_protocol. \
    socket_address import SocketAddress

# front end common exceptions
from spinn_front_end_common.utilities import exceptions as \
    front_end_common_exceptions

# neural models
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.builds.if_cond_exp_base \
    import IFCondExpBase as IF_cond_exp
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.builds.if_curr_dual_exp_base \
    import IFCurrDualExpBase as IF_curr_dual_exp
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.builds.if_curr_exp_base \
    import IFCurrExpBase as IF_curr_exp
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.builds.izk_curr_exp_base \
    import IzkCurrExpBase as IZK_curr_exp
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.builds.izk_cond_exp_base \
    import IzkCondExpBase as IZK_cond_exp

# neural projections
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections \
    .delay_afferent_application_edge import DelayAfferentApplicationEdge
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.utility_models.delay_extension_vertex \
    import DelayExtensionVertex
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.projection_application_edge \
    import ProjectionApplicationEdge

# spike sources
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.spike_source.spike_source_poisson \
    import SpikeSourcePoisson
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.spike_source.spike_source_array \
    import SpikeSourceArray
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.spike_source.spike_source_from_file \
    import SpikeSourceFromFile

# connections
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors.all_to_all_connector \
    import AllToAllConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_number_pre_connector import FixedNumberPreConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_probability_connector import FixedProbabilityConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors.from_list_connector \
    import FromListConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors.from_file_connector \
    import FromFileConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors.multapse_connector \
    import MultapseConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors.one_to_one_connector \
    import OneToOneConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors. \
    distance_dependent_probability_connector import \
    DistanceDependentProbabilityConnector
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neural_projections.connectors. \
    fixed_number_post_connector import FixedNumberPostConnector

# Mechanisms for synapse dynamics
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.synapse_dynamics.pynn_synapse_dynamics \
    import PyNNSynapseDynamics as SynapseDynamics
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.synapse_dynamics.synapse_dynamics_stdp \
    import SynapseDynamicsSTDP as STDPMechanism

# STDP weight dependences
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    .weight_dependence_additive \
    import WeightDependenceAdditive as AdditiveWeightDependence
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence \
    .weight_dependence_multiplicative \
    import WeightDependenceMultiplicative as MultiplicativeWeightDependence

# STDP timing dependences
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    .timing_dependence_spike_pair \
    import TimingDependenceSpikePair as SpikePairRule
# noinspection PyUnresolvedReferences
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    .timing_dependence_pfister_spike_triplet \
    import TimingDependencePfisterSpikeTriplet as PfisterSpikeTripletRule

import spynnaker7

# note importing star is a bad thing to do.
from pyNN.random import *
from pyNN.space import *
import os
import logging

# traditional logger
logger = logging.getLogger(__name__)

# List of binary search paths
_binary_search_paths = []


def register_binary_search_path(search_path):
    """
    :param search_path:
    Registers an additional binary search path for
        for executables

    absolute search path for binaries
    """
    executable_finder.add_path(search_path)


def end():
    """
    Do any necessary cleaning up before exiting.

    Unregisters the controller,
    prints any data recorded using the low-level API
    """
    globals_variables.get_simulator().stop()
    _spinnaker = None


def get_spynnaker():
    """helper method for other plugins to add stuff to the graph

    :return:
    """
    return globals_variables.get_simulator()


def num_processes():
    """ Return the number of MPI processes
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
    globals_variables.get_simulator().reset()


def run(run_time=None):
    """ Run the simulation for run_time ms.

    :param run_time: simulation length (in ms)
    """
    globals_variables.get_simulator().run(run_time)
    return None


def setup(timestep=0.1, min_delay=None, max_delay=None, machine=None,
          database_socket_addresses=None, n_chips_required=None,
          **extra_params):
    """ Should be called at the very beginning of a script.
        extra_params contains any keyword arguments that are required by a\
        given simulator but not by others.

    :param machine: A SpiNNaker machine used to run the simulation.
    :param timestep:
    :param min_delay:
    :param max_delay:
    :param machine:
    :param database_socket_addresses:
    :param n_chips_required: The number of chips required for the simulation
    :param extra_params:
    :return:
    """
    global _binary_search_paths

    logger.info(
        "sPyNNaker (c) {} APT Group, University of Manchester".format(
            __version_year__))
    parent_dir = os.path.split(os.path.split(spynnaker7.__file__)[0])[0]
    logger.info(
        "Release version {}({}) - {} {}. Installed in folder {}".format(
            __version__, __version_name__, __version_month__, __version_year__,
            parent_dir))

    if len(extra_params) > 1:
        logger.warn("Extra params has been applied to the setup command which "
                    "we do not consider")

    spinnaker_control = Spinnaker(
        host_name=machine, timestep=timestep, min_delay=min_delay,
        max_delay=max_delay,
        database_socket_addresses=database_socket_addresses,
        n_chips_required=n_chips_required)
    globals_variables.set_simulator(spinnaker_control)
    # the PyNN API expects the MPI rank to be returned
    return rank()


def set_number_of_neurons_per_core(neuron_type, max_permitted):
    """ Sets a ceiling on the number of neurons of a given type that can be\
        placed on a single core.
    :param neuron_type:
    :param max_permitted:
    """
    if not inspect.isclass(neuron_type):
        if neuron_type in globals():
            neuron_type = globals()[neuron_type]
        else:
            raise Exception("Unknown Vertex Type {}"
                            .format(neuron_type))

    if hasattr(neuron_type, "set_model_max_atoms_per_core"):
        neuron_type.set_model_max_atoms_per_core(max_permitted)
    else:
        raise Exception("{} is not a Vertex type"
                        .format(neuron_type))


def register_database_notification_request(hostname, notify_port, ack_port):
    """ Adds a socket system which is registered with the notification protocol

    :param hostname:
    :param notify_port:
    :param ack_report:
    :return:
    """
    globals_variables.get_simulator()._add_socket_address(
        SocketAddress(hostname, notify_port, ack_port))


# noinspection PyPep8Naming
def Population(size, cellclass, cellparams, structure=None, label=None):
    """

    :param size:
    :param cellclass:
    :param cellparams:
    :param structure:
    :param label:
    :return:
    """
    return globals_variables.get_simulator().create_population(
        size, cellclass, cellparams, structure, label)


# noinspection PyPep8Naming
def Projection(presynaptic_population, postsynaptic_population,
               connector, source=None, target='excitatory',
               synapse_dynamics=None, label=None, rng=None):
    """

    :param presynaptic_population:
    :param postsynaptic_population:
    :param connector:
    :param source:
    :param target:
    :param synapse_dynamics:
    :param label:
    :param rng:
    :return:
    """

    return globals_variables.get_simulator().create_projection(
        presynaptic_population, postsynaptic_population, connector, source,
        target, synapse_dynamics, label, rng)


def NativeRNG(seed_value):
    """ Fixes the random number generator's seed
    :param seed_value:
    :return:
    """
    numpy.random.seed(seed_value)


def get_current_time():
    """
    returns the machine time step defined in setup
    :return:
    """
    return globals_variables.get_simulator().get_current_time()


# =============================================================================
#  Low-level API for creating, connecting and recording from individual neurons
# =============================================================================

def create(cellclass, cellparams=None, n=1):
    """ Create n cells all of the same type.

    If n > 1, return a list of cell ids/references.
    If n==1, return just the single id.
    """
    if cellparams is None:
        cellparams = {}
    return Population(n, cellclass, cellparams)


def connect(source, target, weight=0.0, delay=None, synapse_type="excitatory",
            p=1, rng=None):
    """ Connect a source of spikes to a synaptic target.

    source and target can both be individual cells or lists of cells, in
    which case all possible connections are made with probability p, using
    either the random number generator supplied, or the default rng
    otherwise. Weights should be in nA or uS.
    """
    connector = FixedProbabilityConnector(p_connect=p, weights=weight,
                                          delays=delay)
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
    return globals_variables.get_simulator().min_supported_delay


def get_max_delay():
    """ The maximum allowed synaptic delay.
    :return:
    """
    return globals_variables.get_simulator().max_supported_delay


def set(cells, param, val=None):  # @ReservedAssignment
    """ Set one or more parameters of an individual cell or list of cells.

    param can be a dict, in which case val should not be supplied, or a string
    giving the parameter name, in which case val is the parameter value.
    """
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
    if isinstance(globals_variables.get_simulator(), FailedState):
        raise front_end_common_exceptions.ConfigurationException(
            "You need to have ran setup to get access to the spinnaker machine"
            "object.")
    else:
        return globals_variables.get_simulator().machine
