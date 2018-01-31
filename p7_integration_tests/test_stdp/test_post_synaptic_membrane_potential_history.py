import spynnaker7.pyNN as p
from p7_integration_tests.base_test_case import BaseTestCase
import numpy
import math
import unittest


class TestSTDPPairAdditive(BaseTestCase):

    def test_potentiation_and_depression(self):
        p.setup(1)
        runtime = 100
        initial_run = 1000  # to negate any initial conditions

        # STDP parameters
        a_plus = 0.01
        a_minus = 0.01
        tau_plus = 20
        tau_minus = 20
        plastic_delay = 3
        initial_weight = 2.5
        max_weight = 5
        min_weight = 0



        # -------------------------------------------------------------
        # Learning Parameters:
        accDecayPerSecond      = 1.0
        # Excitatory:
        potentiationRateExcit  = 0.0 # 1.0 # SD! was 0.8
        accPotThresholdExcit   = 20
        depressionRateExcit    = 0.0 # was 0.11 # 0.0  # was 0.4
        accDepThresholdExcit   = -18
        meanPreWindowExcit     = 15.0 # 8
        meanPostWindowExcit    = 1.0 # 8
        maxWeightExcit         = 1.80
        minWeightExcit         = 0.00
        # Excitatory2:
        potentiationRateExcit2 = 0.0 # 1.0 # SD! was 0.8
        accPotThresholdExcit2  = 2
        depressionRateExcit2   = 0.0 # was 0.11 # 0.0  # was 0.4
        accDepThresholdExcit2  = -8
        meanPreWindowExcit2    = 15.0 # 8
        meanPostWindowExcit2   = 1.0 # 8
        maxWeightExcit2        = 1.80
        minWeightExcit2        = 0.00
        # Inhibitory:
        potentiationRateInhib  = 0.0
        accPotThresholdInhib   = 5
        depressionRateInhib    = 0.0
        accDepThresholdInhib   = -5
        meanPreWindowInhib     = 10.0
        meanPostWindowInhib    = 10.0
        maxWeightInhib         = 1.00  # was 0.1
        minWeightInhib         = 0.00
        # Inhibitory2:
        potentiationRateInhib2 = 0.0
        accPotThresholdInhib2  = 5
        depressionRateInhib2   = 0.0
        accDepThresholdInhib2  = -5
        meanPreWindowInhib2    = 10.0
        meanPostWindowInhib2   = 10.0
        maxWeightInhib2        = 1.00  # was 0.1
        minWeightInhib2        = 0.00

        dendriticDelayFraction = 1.0
        # ------------------------------------------------------------


        spike_times = [30, 50, 98]
        spike_times2 = [20, 30, 35, 40, 45, 50, 55,  60, 62]

        for i in range(len(spike_times)):
            spike_times[i] += initial_run

        for i in range(len(spike_times2)):
            spike_times2[i] += initial_run

        # Spike source to send spike via plastic synapse
        pop_src1 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times}, label="src1")

        # Spike source to send spike via static synapse to make
        # post-plastic-synapse neuron fire
        pop_src2 = p.Population(1, p.SpikeSourceArray,
                                {'spike_times': spike_times2}, label="src2")

        # Post-plastic-synapse population
        pop_exc = p.Population(1, p.extra_models.IF_curr_comb_exp_2E2I,{},  label="test")

        # Create projections
        p.Projection(
            pop_src1, pop_exc, p.OneToOneConnector(weights=5.0, delays=1),
            target="excitatory")

        p.Projection(
            pop_src2, pop_exc, p.OneToOneConnector(weights=15.0, delays=1), target="excitatory")


        syn_plas = p.STDPMechanism(
             timing_dependence = p.extra_models.RecurrentRule( accum_decay = accDecayPerSecond,
                    accum_dep_thresh_excit  = accDepThresholdExcit, accum_pot_thresh_excit  = accPotThresholdExcit,
                       pre_window_tc_excit  = meanPreWindowExcit,     post_window_tc_excit  = meanPostWindowExcit,
                    accum_dep_thresh_excit2 = accDepThresholdExcit2, accum_pot_thresh_excit2 = accPotThresholdExcit2,
                       pre_window_tc_excit2 = meanPreWindowExcit2,     post_window_tc_excit2 = meanPostWindowExcit2,
                    accum_dep_thresh_inhib  = accDepThresholdInhib, accum_pot_thresh_inhib  = accPotThresholdInhib,
                       pre_window_tc_inhib  = meanPreWindowInhib,     post_window_tc_inhib  = meanPostWindowInhib,
                    accum_dep_thresh_inhib2 = accDepThresholdInhib2, accum_pot_thresh_inhib2 = accPotThresholdInhib2,
                       pre_window_tc_inhib2 = meanPreWindowInhib2,     post_window_tc_inhib2 = meanPostWindowInhib2),

             #weight_dependence = p.extra_models.WeightDependenceRecurrent(),
             weight_dependence = p.extra_models.WeightDependenceRecurrent(
               w_min_excit = minWeightExcit, w_max_excit = maxWeightExcit, A_plus_excit = potentiationRateExcit, A_minus_excit = depressionRateExcit,
               w_min_excit2 = minWeightExcit2, w_max_excit2 = maxWeightExcit2, A_plus_excit2 = potentiationRateExcit2, A_minus_excit2 = depressionRateExcit2,
               w_min_inhib = minWeightInhib, w_max_inhib = maxWeightInhib, A_plus_inhib = potentiationRateInhib, A_minus_inhib = depressionRateInhib,
               w_min_inhib2 = minWeightInhib2, w_max_inhib2 = maxWeightInhib2, A_plus_inhib2 = potentiationRateInhib2, A_minus_inhib2 = depressionRateInhib2),
             dendritic_delay_fraction = dendriticDelayFraction)

        plastic_synapse = p.Projection(pop_src1, pop_exc,
                                       p.OneToOneConnector(weights=1, delays=2),
                                       synapse_dynamics=p.SynapseDynamics(slow=syn_plas
                                                                          ))


        pop_src1.record()
        pop_exc.record()
        pop_exc.record_v()
        p.run(initial_run + runtime)
        weights = []

        weights.append(plastic_synapse.getWeights())

        pre_spikes = pop_src1.getSpikes()
        v = pop_exc.get_v()
        spikes = pop_exc.getSpikes()

#         potentiation_time_1 = (spikes.segments[0].spiketrains[0].magnitude[0] +
#                                plastic_delay) - spike_times[0]
#         potentiation_time_2 = (spikes.segments[0].spiketrains[0].magnitude[1] +
#                                plastic_delay) - spike_times[0]
#
#         depression_time_1 = spike_times[1] - (
#             spikes.segments[0].spiketrains[0].magnitude[0] + plastic_delay)
#         depression_time_2 = spike_times[1] - (
#             spikes.segments[0].spiketrains[0].magnitude[1] + plastic_delay)
#
#         potentiation_1 = max_weight * a_plus * \
#             math.exp(-potentiation_time_1/tau_plus)
#         potentiation_2 = max_weight * a_plus * \
#             math.exp(-potentiation_time_2/tau_plus)
#
#         depression_1 = max_weight * a_minus * \
#             math.exp(-depression_time_1/tau_minus)
#         depression_2 = max_weight * a_minus * \
#             math.exp(-depression_time_2/tau_minus)
#
#         new_weight_exact = (initial_weight + potentiation_1 + potentiation_2
#                             - depression_1 - depression_2)
#
#         print "Pre neuron spikes at: {}".format(spike_times)
#         print "Post-neuron spikes at: {}".format(
#                         spikes.segments[0].spiketrains[0].magnitude)
#         print "Potentiation time differences: {}, {},\
#              \nDepression time difference: {}, {}".format(
#                     potentiation_time_1, potentiation_time_2,
#                     depression_time_1, depression_time_2)
#         print "Ammounts to potentiate: {}, {},\
#             \nAmount to depress: {}, {},".format(
#             potentiation_1, potentiation_2, depression_1, depression_2)
#         print "New weight exact: {}".format(new_weight_exact)
#         print "New weight SpiNNaker: {}".format(weights[0])
#
#         self.assertTrue(numpy.allclose(weights[0],
#                                        new_weight_exact, atol=0.001))

        import plot_utils
        print pre_spikes
        print spikes
        plot_utils.line_plot(v)
#         p.end()


if __name__ == '__main__':
    unittest.main()
