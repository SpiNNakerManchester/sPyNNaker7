from spynnaker.pyNN.models.neural_projections.connectors \
    import DistanceDependentProbabilityConnector as \
    CommonDistanceDependentProbabilityConnector
from pyNN.space import Space


class DistanceDependentProbabilityConnector(
        CommonDistanceDependentProbabilityConnector):
    """ Make connections using a distribution which varies with distance.
    """

    def __init__(
            self, d_expression, weights=0.0, delays=1,
            allow_self_connections=True, space=Space(),
            safe=True, verbose=False, n_connections=None):
        """

        :param `string` d_expression: \
            the right-hand side of a valid python expression for\
            probability, involving 'd', e.g. "exp(-abs(d))", or "d<3",\
            that can be parsed by eval(), that computes the distance\
            dependent distribution
        :param `bool` allow_self_connections: \
            if the connector is used to connect a\
            Population to itself, this flag determines whether a neuron is\
            allowed to connect to itself, or only to other neurons in the\
            Population.
        :param `pyNN.Space` space: \
            a Space object, needed if you wish to specify distance-\
            dependent weights or delays
        :param `int` n_connections: \
            The number of efferent synaptic connections per neuron.
        :param safe: if True, check that weights and delays have valid values.\
            If False, this check is skipped.
        :param `float` weights: \
            may either be a float, a !RandomDistribution object, a list/\
            1D array with at least as many items as connections to be\
            created, or a distance dependence as per a d_expression. Units nA.
        :param `float` delays:  -- as `weights`. If `None`, all synaptic\
            delays will be set to the global minimum delay.
        """

        super(DistanceDependentProbabilityConnector, self).__init__(
            d_expression=d_expression,
            allow_self_connections=allow_self_connections, safe=safe,
            verbose=verbose, n_connections=n_connections)
        self.set_weights_and_delays(weights, delays)
        self.set_space(space)
