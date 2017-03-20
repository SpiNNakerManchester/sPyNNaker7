from pyNN.space import Space
from pyNN.random import RandomDistribution

from spynnaker.pyNN.models.neural_projections.connectors\
    .one_to_one_connector import OneToOneConnector as CommonOneToOneConnector

class OneToOneConnector(CommonOneToOneConnector):
    """
    Where the pre- and postsynaptic populations have the same size, connect
    cell i in the presynaptic pynn_population.py to cell i in the postsynaptic
    pynn_population.py for all i.
    """

    def __init__(
            self, space=Space(), safe=True, verbose=False, weights=0.0,
            delays=1):
        """
        """
        CommonOneToOneConnector.__init__(
            self, safe=safe, verbose=verbose,
            random_number_class=RandomDistribution)
        self.set_weights_and_delays(weights, delays)
        self.set_space(space)

