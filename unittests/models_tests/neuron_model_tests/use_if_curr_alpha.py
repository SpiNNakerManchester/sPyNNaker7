import spynnaker7.pyNN as p
p.setup(0.1)

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [[5, 10, 15, 20]]}, label="src1")

pop_ex = p.Population(1, p.IF_curr_alpha, {}, label="test")
# pop_ex.set("tau_syn_E", 3)
# pop_ex.set("tau_syn_I", 4)

# define the projection
exc_proj = p.Projection(pop_src1, pop_ex,
                        p.OneToOneConnector(weights=1, delays=1),
                        target="excitatory")
inh_proj = p.Projection(pop_src1, pop_ex,
                        p.OneToOneConnector(weights=1, delays=20),
                        target="inhibitory")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
p.run(50)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

p.end()
print "\n job done"
