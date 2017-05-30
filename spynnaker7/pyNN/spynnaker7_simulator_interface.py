from six import add_metaclass

from spinn_utilities.abstract_base import AbstractBase
from spinn_utilities.abstract_base import abstractmethod

from spynnaker.pyNN.spynnaker_simulator_interface \
    import SpynnakerSimulatorInterface


@add_metaclass(AbstractBase)
class Spynnaker7SimulatorInterface(SpynnakerSimulatorInterface):

    __slots__ = ()

    @abstractmethod
    def create_population(self, size, cellclass, cellparams, structure,
                          label):
        pass

    @abstractmethod
    def create_projection(self, presynaptic_population,
                          postsynaptic_population, connector, source,
                          target, synapse_dynamics, label, rng):
        pass
