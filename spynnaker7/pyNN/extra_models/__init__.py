# spynnaker 8 extra models
from spynnaker.pyNN.models.neuron.builds import IFCondExpStoc
from spynnaker.pyNN.models.neuron.builds import IFCurrDelta
from spynnaker.pyNN.models.neuron.builds import IFCurrExpCa2Adaptive
from spynnaker.pyNN.models.neuron.builds import IzkCondExpBase as IZK_cond_exp
from spynnaker.pyNN.models.neuron.builds import IzkCurrExpBase as IZK_curr_exp
from spynnaker.pyNN.models.neuron.builds\
    import IFCurrDualExpBase as IF_curr_dual_exp

# plastic timing spynnaker 7
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceRecurrent as RecurrentRule
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceSpikeNearestPair as SpikeNearestPair
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependenceVogels2011 as Vogels2011Rule
from spynnaker.pyNN.models.neuron.plasticity.stdp.timing_dependence \
    import TimingDependencePfisterSpikeTriplet as PfisterSpikeTriplet

# plastic weight spynnaker 7
from spynnaker7.pyNN.models.plasticity_components.weight_dependence \
    .weight_dependence_additive_triplet \
    import WeightDependenceAdditiveTriplet as AdditiveTripletWeightDependence


# custom plasticity models
# from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence.
#    import 

__all__ = [
    # spynnaker 7 models
    'IFCurrDelta', 'IFCurrExpCa2Adaptive', 'IFCondExpStoc',
    'IZK_curr_exp', 'IZK_cond_exp', 'IF_curr_dual_exp',

    # spynnaker 7 plastic stuff
    'AdditiveTripletWeightDependence',
    'PfisterSpikeTriplet',
    'SpikeNearestPair',
    'RecurrentRule', 'Vogels2011Rule']
