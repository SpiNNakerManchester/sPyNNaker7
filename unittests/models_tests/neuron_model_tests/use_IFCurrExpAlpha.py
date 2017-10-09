import spynnaker7.pyNN as p
import python.plot_utils
p.setup(0.1)

pop_src1 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[5, 15, 20, 30]]}, label="src1")


pop_ex = p.Population(1, p.IF_curr_exp_alpha, {}, label="test")
pop_ex.set("exc_tau", 2)
# define the projection
exc_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=1), target="excitatory")
inh_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=100), target="inhibitory")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
p.run(200)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"