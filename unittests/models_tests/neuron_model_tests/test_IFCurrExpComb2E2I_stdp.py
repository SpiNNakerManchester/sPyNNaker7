import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(1)


pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1, 55]]}, label="src")
#pop_src_plastic = p.Population(1, p.SpikeSourceArray, {'spike_times': [[]]}, label="src")

pop_ex = p.Population(1, p.extra_models.IF_curr_comb_exp_2E2I, {}, label="test")
#pop_ex = p.Population(1, p.IF_curr_exp, {}, label="test")

# define the projection
#exc_proj = p.Projection(pop_src, pop_ex,
#        p.OneToOneConnector(weights=1, delays=2), target="excitatory")

pop_ex.set('exc_a_tau', 10)
pop_ex.set('exc_b_tau', 5)
pop_ex.set('exc2_a_tau', 10)
pop_ex.set('exc2_b_tau', 5)
pop_ex.set('inh_a_tau', 10)
pop_ex.set('inh_b_tau', 5)
pop_ex.set('inh2_a_tau', 20)
pop_ex.set('inh2_b_tau', 5)

syn_plas = p.STDPMechanism(
     timing_dependence = p.extra_models.RecurrentRule(),
#       accum_decay = accDecayPerSecond,
#             accum_dep_thresh_excit  = accDepThresholdExcit, accum_pot_thresh_excit  = accPotThresholdExcit,
#                pre_window_tc_excit  = meanPreWindowExcit,     post_window_tc_excit  = meanPostWindowExcit,
#             accum_dep_thresh_excit2 = accDepThresholdExcit2, accum_pot_thresh_excit2 = accPotThresholdExcit2,
#                pre_window_tc_excit2 = meanPreWindowExcit2,     post_window_tc_excit2 = meanPostWindowExcit2,
#             accum_dep_thresh_inhib  = accDepThresholdInhib, accum_pot_thresh_inhib  = accPotThresholdInhib,
#                pre_window_tc_inhib  = meanPreWindowInhib,     post_window_tc_inhib  = meanPostWindowInhib,
#             accum_dep_thresh_inhib2 = accDepThresholdInhib2, accum_pot_thresh_inhib2 = accPotThresholdInhib2,
#                pre_window_tc_inhib2 = meanPreWindowInhib2,     post_window_tc_inhib2 = meanPostWindowInhib2),

     weight_dependence = p.extra_models.WeightDependenceRecurrent())
#      weight_dependence = p.extra_models.WeightDependenceRecurrent(
#        w_min_excit = minWeightExcit, w_max_excit = maxWeightExcit, A_plus_excit = potentiationRateExcit, A_minus_excit = depressionRateExcit,
#        w_min_excit2 = minWeightExcit2, w_max_excit2 = maxWeightExcit2, A_plus_excit2 = potentiationRateExcit2, A_minus_excit2 = depressionRateExcit2,
#        w_min_inhib = minWeightInhib, w_max_inhib = maxWeightInhib, A_plus_inhib = potentiationRateInhib, A_minus_inhib = depressionRateInhib,
#        w_min_inhib2 = minWeightInhib2, w_max_inhib2 = maxWeightInhib2, A_plus_inhib2 = potentiationRateInhib2, A_minus_inhib2 = depressionRateInhib2),
#      dendritic_delay_fraction = dendriticDelayFraction)
#
#
# syn_plas = p.STDPMechanism(
#     timing_dependence=p.SpikePairRule(tau_plus=20.0, tau_minus=20.0),
#     weight_dependence=p.AdditiveWeightDependence(w_min=0, w_max=5.0, A_plus=0.5, A_minus=0.5)
#     )

proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.OneToOneConnector(weights=2.5, delays=1),
    synapse_dynamics=p.SynapseDynamics(slow=syn_plas),
    target="excitatory")

inh_proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.OneToOneConnector(weights=1.75, delays=5),
    synapse_dynamics=p.SynapseDynamics(slow=syn_plas),
    target="inhibitory2")


#exc2_proj = p.Projection(pop_src, pop_ex,
#        p.OneToOneConnector(weights=1, delays=30), target="excitatory2")

#inh_proj = p.Projection(pop_src, pop_ex,
#        p.OneToOneConnector(weights=1, delays=20), target="inhibitory")

#inh2_proj2 = p.Projection(pop_src, pop_ex,
#        p.OneToOneConnector(weights=1, delays=40), target="inhibitory2")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()

for i in range(1):
    p.run(50)
    exc_w = proj.getWeights()
    inh_w = inh_proj.getWeights()
    print "exc weight: {}".format(exc_w)
    print "inh weight: {}".format(inh_w)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"