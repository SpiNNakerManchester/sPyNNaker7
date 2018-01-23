import logging

from pyNN.space import Space

from pyNN.random import RandomDistribution

from spynnaker.pyNN.models.neural_projections.connectors \
    import FixedNumberPostConnector as CommonFixedNumberPostConnector

logger = logging.getLogger(__file__)


class FixedNumberPostConnector(CommonFixedNumberPostConnector):
    """ pynn connector that puts a fixed number of connections on each of the\
        post neurons
    """

    def __init__(
            self, n, weights=0.0, delays=1, allow_self_connections=True,
            space=Space(), safe=True, verbose=False):
        """

        :param n: \
            number of random post-synaptic neurons connected to output
        :param allow_self_connections: \
            if the connector is used to connect a\
            Population to itself, this flag determines whether a neuron is\
            allowed to connect to itself, or only to other neurons in the\
            Population.
        :param space: a Space object, needed if you wish to specify distance-\
            dependent weights or delays
        :param safe: if True, check that weights and delays have valid values.\
            If False, this check is skipped.
        :param verbose: ??????????
        :param `float` weights: \
            may either be a float, a !RandomDistribution object, a list/\
            1D array with at least as many items as connections to be\
            created, or a distance dependence as per a d_expression. Units nA.
        :param `float` delays:  -- as `weights`. If `None`, all synaptic\
            delays will be set to the global minimum delay.
        """
        if isinstance(n, RandomDistribution):
            raise NotImplementedError(
                "RandomDistribution is not supported for n in the"
                " implementation of FixedNumberPostConnector on this platform")

        super(FixedNumberPostConnector, self).__init__(
            n=n, safe=safe, verbose=verbose,
            allow_self_connections=allow_self_connections)

        self.set_weights_and_delays(weights, delays)
        self.set_space(space)
