from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence.\
    timing_dependence_spike_pair import \
    TimingDependenceSpikePair as CommonTimingDependenaceSpikePair


class TimingDependenceSpikePair(CommonTimingDependenaceSpikePair):

    def __init__(self, tau_plus=20.0, tau_minus=20.0, tau_c=None, tau_d=None):
        CommonTimingDependenaceSpikePair.__init__(
            self, tau_plus=tau_plus, tau_minus=tau_minus,
            tau_c=tau_c, tau_d = tau_d)
