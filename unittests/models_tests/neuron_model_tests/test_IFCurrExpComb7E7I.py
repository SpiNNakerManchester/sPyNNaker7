import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_src_exc = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src_exc")
pop_src_inh = p.Population(1, p.SpikeSourceArray, {'spike_times': [[100]]}, label="src_inh")


pop_ex = p.Population(2, p.extra_models.IF_curr_comb_exp_7E7I, {}, label="test")

d = 10

# #for i in range(5)
# pop_ex.set('exc_a_tau', 1.7)
# pop_ex.set('exc_b_tau', 0.2)
#
# pop_ex.set('exc2_a_tau', 3.7)
# pop_ex.set('exc2_b_tau', 0.7)
#
# pop_ex.set('exc3_a_tau', 4.7)
# pop_ex.set('exc3_b_tau', 0.7)
#
# pop_ex.get('exc3_a_tau', 5.4)
# pop_ex.get('exc3_b_tau', 3.2)
#
# pop_ex.set('exc4_a_tau', 1.2)
# pop_ex.set('exc4_b_tau', 0.3)
#
# pop_ex.set('exc5_a_tau', 4.9)
# pop_ex.set('exc5_b_tau', 0.9)
#
# pop_ex.set('exc6_a_tau', 4.9)
# pop_ex.set('exc6_b_tau', 0.9)
#
# pop_ex.set('exc7_a_tau', 4.9)
# pop_ex.set('exc7_b_tau', 0.9)
#
# pop_ex.set('inh_a_tau', 5.1)
# pop_ex.set('inh_b_tau', 0.1)
#
# pop_ex.set('inh2_a_tau', 3.7)
# pop_ex.set('inh2_b_tau', 0.7)
#
# pop_ex.set('inh3_a_tau', 2.4)
# pop_ex.set('inh3_b_tau', 1)
#
# pop_ex.set('inh4_a_tau', 6.9)
# pop_ex.set('inh4_b_tau', 1.9)
#
# pop_ex.set('inh5_a_tau', 1.7)
# pop_ex.set('inh5_b_tau', 0.7)
#
# pop_ex.set('inh6_a_tau', 1.7)
# pop_ex.set('inh6_b_tau', 0.7)
#
# pop_ex.set('inh7_a_tau', 1.7)
# pop_ex.set('inh7_b_tau', 0.7)

exc_proj = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=0), target="excitatory", label="projTemp")
exc_proj2 = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=2*d), target="excitatory2")
exc_proj3 = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=4*d), target="excitatory3")
exc_proj4 = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=6*d), target="excitatory4")
exc_proj5 = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=8*d), target="excitatory5")
exc_proj6 = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=10*d), target="excitatory6")
exc_proj7 = p.Projection(pop_src_exc, pop_ex,
        p.OneToOneConnector(weights=1, delays=12*d), target="excitatory7")

inh_proj = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=0*d), target="inhibitory")
inh_proj2 = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=2*d), target="inhibitory2")
inh_proj3 = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=4*d), target="inhibitory3")
inh_proj4 = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=6*d), target="inhibitory4")
inh_proj5 = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=8*d), target="inhibitory5")
inh_proj6 = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=10*d), target="inhibitory6")
inh_proj7 = p.Projection(pop_src_inh, pop_ex,
        p.OneToOneConnector(weights=1, delays=12*d), target="inhibitory7")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
p.run(300)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"