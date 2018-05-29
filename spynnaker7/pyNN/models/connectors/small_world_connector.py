from pyNN.space import Space

from spynnaker.pyNN.models.neural_projections.connectors \
    import SmallWorldConnector as CommonSmallWorldConnector


class SmallWorldConnector(CommonSmallWorldConnector):

    def __init__(
            self, degree, rewiring, weights=0.0,
            delays=1, allow_self_connections=True, space=Space(),
            safe=True, verbose=False, n_connections=None):
        super(SmallWorldConnector, self).__init__(
            degree=degree, rewiring=rewiring,
            allow_self_connections=allow_self_connections, safe=safe,
            verbose=verbose, n_connections=n_connections)
        self.set_weights_and_delays(weights, delays)
        self.set_space(space)

    def set_weights_and_delays(self, weights, delays):
        self._weights = weights
        self._delays = delays

    def get_weight(self):
        return self._weights

    def get_delay(self):
        return self._delay
