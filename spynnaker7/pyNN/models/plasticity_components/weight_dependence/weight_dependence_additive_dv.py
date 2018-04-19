from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence.\
    weight_dependence_additive_dv import WeightDependenceAdditiveDvDt as \
    CommonWeightDependenceAdditiveDvDt


class WeightDependenceAdditiveDvDt(CommonWeightDependenceAdditiveDvDt):

    # noinspection PyPep8Naming
    def __init__(
            self, w_min=0.0, w_max=1.0, scale=0.01):
        CommonWeightDependenceAdditiveDvDt.__init__(self, w_min=w_min, w_max=w_max)
        self.scale = scale
