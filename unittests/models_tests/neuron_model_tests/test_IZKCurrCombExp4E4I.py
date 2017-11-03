import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src")


pop_ex = p.Population(1, p.extra_models.IZK_curr_comb_exp_4E4I, {}, label="test")

d = 12

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
# print pop_ex.get('exc3_a_A')
# print pop_ex.get('exc3_b_B')
# print pop_ex.get('exc3_a_tau')
# print pop_ex.get('exc3_b_tau')
#
# pop_ex.set('exc4_a_tau', 1.2)
# pop_ex.set('exc4_b_tau', 0.3)
#
# pop_ex.set('exc5_a_tau', 4.9)
# pop_ex.set('exc5_b_tau', 0.9)
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



exc_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=1*d), target="excitatory", label="projTemp")
exc_proj2 = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=3*d), target="excitatory2")
exc_proj3 = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=5*d), target="excitatory3")
exc_proj4 = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=7*d), target="excitatory4")

inh_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=2*d), target="inhibitory")
inh_proj2 = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=4*d), target="inhibitory2")
inh_proj3 = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=6*d), target="inhibitory3")
inh_proj4 = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=1, delays=8*d), target="inhibitory4")


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