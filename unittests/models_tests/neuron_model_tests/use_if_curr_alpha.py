import spynnaker7.pyNN as p
p.setup(0.1)

pop_src1 = p.Population(256, p.SpikeSourceArray,
                        {'spike_times': [5, 10, 15, 20]}, label="src1")

pop_ex = p.Population(256, p.IF_curr_alpha, {}, label="test")

exc_proj = p.Projection(pop_src1, pop_ex,
                        p.OneToOneConnector(weights=1, delays=1),
                        target="excitatory")

inh_proj = p.Projection(pop_src1, pop_ex,
                        p.OneToOneConnector(weights=1, delays=14),
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
