import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_ex = p.Population(5, p.extra_models.IF_curr_comb_exp, {}, label="test")
pop_src1 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1, 2]]}, label="src1")
#pop_src2 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1]]}, label="src1")
#pop_src3 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1]]}, label="src1")
#pop_src4 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[1]]}, label="src1")

#IFCurrCombExp.set_excitatory_scalar()

pop_ex2 = p.Population(10, p.extra_models.IF_curr_comb_exp_2E2I, {}, label="test")

pop_ex.set('exc_a_tau', 5.0)
pop_ex.set('exc_b_tau', 0.01)

# define the projection
exc_proj = p.Projection(pop_src1, pop_ex,
        #p.OneToOneConnector(weights=1, delays=10), target="excitatory")
        p.AllToAllConnector(weights=1, delays=0.6), target="excitatory")

exc3_proj = p.Projection(pop_src1, pop_ex2,
        #p.OneToOneConnector(weights=1, delays=10), target="excitatory")
        p.AllToAllConnector(weights=1, delays=0.6), target="excitatory2")
exc2_proj = p.Projection(pop_src1, pop_ex2,
        #p.OneToOneConnector(weights=1, delays=10), target="excitatory")
        p.AllToAllConnector(weights=1, delays=0.6), target="excitatory")
exc3_proj = p.Projection(pop_src1, pop_ex2,
        #p.OneToOneConnector(weights=1, delays=10), target="excitatory")
        p.AllToAllConnector(weights=1, delays=0.6), target="excitatory")

inh_proj = p.Projection(pop_ex, pop_ex2,
        p.OneToOneConnector(weights=1, delays=0.4), target="inhibitory")

inh_proj2 = p.Projection(pop_ex2, pop_ex2,
        p.AllToAllConnector(weights=1, delays=0.4), target="excitatory2")
inh_proj2 = p.Projection(pop_ex2, pop_ex2,
        p.AllToAllConnector(weights=1, delays=0.4), target="inhibitory2")


pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
p.run(50)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"