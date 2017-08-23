import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(1)


pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1, 51, 101, 151, 201 ]]}, label="src")
#pop_src_plastic = p.Population(1, p.SpikeSourceArray, {'spike_times': [[]]}, label="src")

pop_ex = p.Population(100, p.extra_models.IF_curr_comb_exp_2E2I, {}, label="test")
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
    timing_dependence=p.SpikePairRule(tau_plus=20.0, tau_minus=20.0),
    weight_dependence=p.AdditiveWeightDependence(w_min=0, w_max=5.0, A_plus=0.5, A_minus=0.5)
    )

proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.AllToAllConnector(weights=2.5, delays=1),
    synapse_dynamics=p.SynapseDynamics(slow=syn_plas),
    target="excitatory")


inh_proj = p.Projection(
    pop_src, #_plastic,
    pop_ex,
    p.OneToOneConnector(weights=0.1, delays=5),
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
for i in range(10):
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