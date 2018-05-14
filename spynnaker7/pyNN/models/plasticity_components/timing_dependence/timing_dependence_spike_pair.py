from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence import (
    TimingDependenceSpikePair as
    CommonTimingDependenaceSpikePair)


class TimingDependenceSpikePair(CommonTimingDependenaceSpikePair):

    def __init__(self, tau_plus=20.0, tau_minus=20.0):
        super(TimingDependenceSpikePair, self).__init__(
            tau_plus=tau_plus, tau_minus=tau_minus)
