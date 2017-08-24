import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(.1)

pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src")

pop_ex = p.Population(1, p.extra_models.IF_curr_comb_exp_2E2I, {}, label="test")

# define projections
exc_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=1), target="excitatory")

exc2_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=30), target="excitatory2")

inh_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=20), target="inhibitory")

inh2_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=40), target="inhibitory2")


pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
p.run(100)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"