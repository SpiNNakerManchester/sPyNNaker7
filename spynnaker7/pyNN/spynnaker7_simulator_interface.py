from six import add_metaclass

from spinn_utilities.abstract_base import AbstractBase, abstractmethod

from spynnaker.pyNN.spynnaker_simulator_interface \
    import SpynnakerSimulatorInterface


@add_metaclass(AbstractBase)
class Spynnaker7SimulatorInterface(SpynnakerSimulatorInterface):

    __slots__ = ()

    @abstractmethod
    def create_population(self, size, cellclass, cellparams, structure,
                          label):
        """ Creates a PyNN 0.75 population

        :param size: the number of neurons in this population
        :param cellclass: the type of neuron model this pop represents
        :param cellparams: the neuron parameters for this population
        :param structure: defines where the neurons are located in space
        :param label: the human readable label of the population
        :return: a population instance
        """

    @abstractmethod
    def create_projection(self, presynaptic_population,
                          postsynaptic_population, connector, source,
                          target, synapse_dynamics, label, rng):
        """ Create a PyNN 0.75 projection

        :param presynaptic_population: \
            source population this projection goes from
        :param postsynaptic_population: \
            destination population this projection goes to
        :param connector: the definition of which neurons connect to each other
        :param source: the originating variable of the source population model
        :param target: type of projection
        :param synapse_dynamics: plasticity object
        :param label: human readable version of the projection
        :param rng: the random number generator to use on this projection
        :return: a projection instance
        """
