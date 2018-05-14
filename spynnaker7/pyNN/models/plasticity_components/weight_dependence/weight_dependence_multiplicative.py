from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence import (
    WeightDependenceMultiplicative as
    CommonWeightDependenceMultiplicative)


class WeightDependenceMultiplicative(CommonWeightDependenceMultiplicative):

    def __init__(self, w_min=0.0, w_max=1.0, A_plus=0.01, A_minus=0.01):
        super(WeightDependenceMultiplicative, self).__init__(
            w_min=w_min, w_max=w_max)
        self.set_a_plus_a_minus(a_plus=A_plus, a_minus=A_minus)
