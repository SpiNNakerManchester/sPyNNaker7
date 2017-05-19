from spinn_front_end_common.utilities import exceptions
from spynnaker.pyNN.utilities.spynnaker_failed_state \
    import SpynnakerFailedState
from spynnaker7.pyNN.spynnaker7_simulator_interface \
    import Spynnaker7SimulatorInterface


class Spynnaker7FailedState(Spynnaker7SimulatorInterface,
                            SpynnakerFailedState):

    __slots__ = ()

    def create_population(self, size, cellclass, cellparams, structure,
                          label):
        raise exceptions.ConfigurationException(
            "This call is only valid between setup and end/stop")

    def create_projection(self, presynaptic_population,
                          postsynaptic_population, connector, source,
                          target, synapse_dynamics, label, rng):
        raise exceptions.ConfigurationException(
            "This call is only valid between setup and end/stop")
