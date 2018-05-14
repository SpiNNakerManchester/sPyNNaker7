import logging
from pyNN.space import Space
from pyNN.random import RandomDistribution
from spynnaker.pyNN.models.neural_projections.connectors import (
    FixedNumberPreConnector as
    CommonFixedNumberPreConnector)

logger = logging.getLogger(__file__)


class FixedNumberPreConnector(CommonFixedNumberPreConnector):
    """ Connects a fixed number of pre-synaptic neurons selected at random,\
        to all post-synaptic neurons
    """

    def __init__(
            self, n, weights=0.0, delays=1, allow_self_connections=True,
            space=Space(), safe=True, verbose=False):
        """
        :param n: \
            number of random pre-synaptic neurons connected to output
        :param allow_self_connections: \
            if the connector is used to connect a\
            Population to itself, this flag determines whether a neuron is\
            allowed to connect to itself, or only to other neurons in the\
            Population.
        :param `pyNN.Space` space: \
            a Space object, needed if you wish to specify distance-\
            dependent weights or delays - not implemented
        :param safe: if True, check that weights and delays have valid values.\
            If False, this check is skipped.
        :param verbose:
        """

        if isinstance(n, RandomDistribution):
            raise NotImplementedError(
                "RandomDistribution is not supported for n in the"
                " implementation of FixedNumberPreConnector on this platform")

        super(FixedNumberPreConnector, self).__init__(
            n=n, safe=safe,
            allow_self_connections=allow_self_connections, verbose=verbose)

        self.set_weights_and_delays(weights, delays)
        self.set_space(space)
