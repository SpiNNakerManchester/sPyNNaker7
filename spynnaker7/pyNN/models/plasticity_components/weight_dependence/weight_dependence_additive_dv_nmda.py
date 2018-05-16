from spynnaker.pyNN.models.neuron.plasticity.stdp.weight_dependence.\
    weight_dependence_additive_dv_nmda import WeightDependenceAdditiveDvDtNMDA as \
    CommonWeightDependenceAdditiveDvDtNMDA


class WeightDependenceAdditiveDvDtNMDA(CommonWeightDependenceAdditiveDvDtNMDA):

    # noinspection PyPep8Naming
    def __init__(
            self, w_min=0.0, w_max=1.0, scale=0.01, boost=0.1, boost_thresh=0.1):
        CommonWeightDependenceAdditiveDvDtNMDA.\
            __init__(self, w_min=w_min, w_max=w_max, boost_thresh=boost_thresh)
        self.scale = scale
        self.boost = boost

