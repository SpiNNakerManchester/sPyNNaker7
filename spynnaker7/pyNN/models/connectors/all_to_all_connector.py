import logging
from pyNN.space import Space
from spynnaker.pyNN.models.neural_projections.connectors import (
    AllToAllConnector as
    CommonAllToAllConnector)

logger = logging.getLogger(__file__)


class AllToAllConnector(CommonAllToAllConnector):
    """ Connects all cells in the presynaptic population to all cells in \
        the postsynaptic population
    """

    def __init__(
            self, weights=0.0, delays=1, allow_self_connections=True,
            space=Space(), safe=True, verbose=None):
        """

        :param allow_self_connections: \
            if the connector is used to connect a\
            Population to itself, this flag determines whether a neuron is\
            allowed to connect to itself, or only to other neurons in the\
            Population.
        :type allow_self_connections: bool
        :param space: a Space object, needed if you wish to specify distance-\
            dependent weights or delays
        :param safe: if True, check that weights and delays have valid values.\
            If False, this check is skipped.
        :param verbose:
        """
        super(AllToAllConnector, self).__init__(
            allow_self_connections=allow_self_connections, safe=safe,
            verbose=verbose)
        self.set_space(space)
        self.set_weights_and_delays(weights, delays)
