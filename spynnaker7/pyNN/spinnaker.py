import logging
from spinn_utilities.overrides import overrides
from pyNN.random import NumpyRNG
from pyNN.random import RandomDistribution
from pyNN import __version__ as pynn_version
from spinn_front_end_common.utilities import globals_variables
from spynnaker.pyNN.abstract_spinnaker_common import AbstractSpiNNakerCommon
from spynnaker.pyNN.spynnaker_simulator_interface import (
    SpynnakerSimulatorInterface)
from spynnaker7.pyNN.models import Population, Projection
from spynnaker7.pyNN.spynnaker7_simulator_interface import (
    Spynnaker7SimulatorInterface)
from spynnaker7.pyNN.utilities.random_stats import (
    RandomStatsScipyImpl, RandomStatsUniformImpl)
from spynnaker7.pyNN.utilities import Spynnaker7FailedState
from ._version import __version__ as version

# global objects
logger = logging.getLogger(__name__)
# At import time change the default FailedState
globals_variables.set_failed_state(Spynnaker7FailedState())


class Spinnaker(AbstractSpiNNakerCommon, Spynnaker7SimulatorInterface):
    """ Spinnaker: the main entrance for the sPyNNaker 7 front end.
    """

    def __init__(
            self, host_name=None, timestep=None, min_delay=None,
            max_delay=None, graph_label=None, database_socket_addresses=None,
            n_chips_required=None):
        front_end_versions = [
            ("sPyNNaker7_version", version),
            ("pyNN_version", pynn_version)]

        # population holders
        super(Spinnaker, self).__init__(
            database_socket_addresses=database_socket_addresses,
            graph_label=graph_label,
            n_chips_required=n_chips_required, timestep=timestep,
            hostname=host_name, max_delay=max_delay, min_delay=min_delay,
            front_end_versions=front_end_versions)

    @overrides(Spynnaker7SimulatorInterface.create_population)
    def create_population(self, size, cellclass, cellparams, structure, label):
        return Population(
            size=size, cellclass=cellclass, cellparams=cellparams,
            structure=structure, label=label, spinnaker=self)

    @overrides(Spynnaker7SimulatorInterface.create_projection)
    def create_projection(
            self, presynaptic_population, postsynaptic_population, connector,
            source, target, synapse_dynamics, label, rng):
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

    @overrides(SpynnakerSimulatorInterface.get_distribution_to_stats)
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

    @overrides(SpynnakerSimulatorInterface.is_a_pynn_random)
    def is_a_pynn_random(self, thing):
        """ Checks if the thing is a PyNN random

        The exact definition of a PyNN random can or could change between\
        PyNN versions so can only be checked against a specific PyNN version

        :param thing: any object
        :return: True if this object is a PyNN random
        :trype: bool
        """
        return isinstance(thing, RandomDistribution)

    @overrides(SpynnakerSimulatorInterface.get_pynn_NumpyRNG)
    def get_pynn_NumpyRNG(self):
        """ Get specific PyNN version of NumpyRNG

        :return: NumpyRNG
        :rtype: NumpyRNG
        """
        return NumpyRNG()
