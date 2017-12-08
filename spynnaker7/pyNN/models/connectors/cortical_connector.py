from spynnaker.pyNN.models.neural_projections.connectors.cortical_connector\
    import CorticalConnector as CommonCorticalConnector
import numpy
from spynnaker.pyNN.models.neural_projections.connectors import ConvolutionKernel

class CorticalConnector(CommonCorticalConnector):
    
    def __init__(self, probability, max_distance, shape_pre, shape_post,
                 shape_common=None, allow_self_connections=True,
                 pre_n_per_zone=1, pre_sample_steps=None, pre_start_coords=None,
                 post_n_per_zone=1, post_sample_steps=None, post_start_coords=None,
                 weights=0.0, delays=1, safe=True,
                 space=None, verbose=False, generate_on_machine=False):

        CommonCorticalConnector.__init__(self,
            probability, max_distance, shape_pre, shape_post, shape_common=shape_common,
            allow_self_connections=allow_self_connections,
            pre_n_per_zone=pre_n_per_zone,
            pre_sample_steps=pre_sample_steps, pre_start_coords=pre_start_coords,
            post_n_per_zone=post_n_per_zone,
            post_sample_steps=post_sample_steps, post_start_coords=post_start_coords,
            weights=weights, delays=delays, safe=safe, space=space,
            verbose=verbose, generate_on_machine=generate_on_machine)

        self._delays = delays.view(ConvolutionKernel) \
                                    if isinstance(delays, numpy.ndarray) else delays
        self._weights = weights.view(ConvolutionKernel) \
                                    if isinstance(weights, numpy.ndarray) else weights
        # self._weights = weights
        # self._delays = delays

        # self.set_weights_and_delays(weights, delays)
        # print("\n\nspynn7 gen on machine = %s\n"%self._gen_on_spinn)