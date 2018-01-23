# common front end imports
import logging

from pyNN.random import NumpyRNG
from pyNN.random import RandomDistribution
from pyNN import __version__ as pynn_version

from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon
from spynnaker7.pyNN.models import Population, Projection
from spynnaker7.pyNN.spynnaker7_simulator_interface import \
    Spynnaker7SimulatorInterface
from spynnaker7.pyNN.utilities.random_stats import \
    RandomStatsScipyImpl, RandomStatsUniformImpl
from spynnaker7.pyNN.utilities import Spynnaker7FailedState
from _version import __version__ as version

# global objects
logger = logging.getLogger(__name__)

# At import time change the default FailedState
globals_variables.set_failed_state(Spynnaker7FailedState())


class Spinnaker(AbstractSpiNNakerCommon, Spynnaker7SimulatorInterface):
    """
    Spinnaker: the main entrance for the spynnaker front end
    """

    def __init__(
            self, host_name=None, timestep=None, min_delay=None,
            max_delay=None, graph_label=None, database_socket_addresses=None,
            n_chips_required=None):
        front_end_versions = [("sPyNNaker7_version", version)]
        front_end_versions.append(("pyNN_version", pynn_version))

        # population holders
        super(Spinnaker, self).__init__(
            database_socket_addresses=database_socket_addresses,
            graph_label=graph_label,
            n_chips_required=n_chips_required, timestep=timestep,
            hostname=host_name, max_delay=max_delay, min_delay=min_delay,
            front_end_versions=front_end_versions)

    def create_population(self, size, cellclass, cellparams, structure, label):
        """ creates a pynn 0.75 population

        :param size: the number of atoms in this population
        :param cellclass: the type of neuron model this pop represents
        :param cellparams: the neuron parameters for this population
        :param structure: something to do with space
        :param label: the human readable label of the population
        :return: a population instance
        """
        return Population(
            size=size, cellclass=cellclass, cellparams=cellparams,
            structure=structure, label=label, spinnaker=self)

    def create_projection(
            self, presynaptic_population, postsynaptic_population, connector,
            source, target, synapse_dynamics, label, rng):
        """

        :param presynaptic_population: source pop this projection goes from
        :param postsynaptic_population: dest pop this projection goes to
        :param connector: the definition of which neurons connect to each other
        :param source:
        :param target: type of projection
        :param synapse_dynamics: plasticity object
        :param label: human readable version of the projection
        :param rng: the random number generator to use on this projection
        :return:
        """
        if label is None:
            label = "Projection {}".format(self._edge_count)
            self._edge_count += 1
        return Projection(
            presynaptic_population=presynaptic_population, label=label,
            postsynaptic_population=postsynaptic_population, rng=rng,
            connector=connector, source=source, target=target,
            synapse_dynamics=synapse_dynamics, spinnaker_control=self,
            machine_time_step=self._machine_time_step,
            timescale_factor=self._time_scale_factor,
            user_max_delay=self.max_delay)

    def get_distribution_to_stats(self):
        return {
            'binomial': RandomStatsScipyImpl("binom"),
            'gamma': RandomStatsScipyImpl("gamma"),
            'exponential': RandomStatsScipyImpl("expon"),
            'lognormal': RandomStatsScipyImpl("lognorm"),
            'normal': RandomStatsScipyImpl("norm"),
            'poisson': RandomStatsScipyImpl("poisson"),
            'uniform': RandomStatsUniformImpl(),
            'randint': RandomStatsScipyImpl("randint"),
            'vonmises': RandomStatsScipyImpl("vonmises")}

    @staticmethod
    def get_random_distribution():
        """ Deprecated. Use is_a_pynn_random instead """
        return RandomDistribution

    def is_a_pynn_random(self, thing):
        """ Checks if the thing is a pynn random

        The exact definition of a pynn random can or could change between\
        pynn versions so can only be checked against a specific pynn version

        :param thing: any object
        :return: True if this object is a pynn random
        :trype: bool
        """
        return isinstance(thing, RandomDistribution)

    def get_pynn_NumpyRNG(self):
        """ Get specific PyNN version of NumpyRNG

        :return: NumpyRNG
        :rtype: NumpyRNG
        """
        return NumpyRNG()
