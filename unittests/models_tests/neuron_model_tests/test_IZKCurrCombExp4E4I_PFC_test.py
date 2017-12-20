import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_src = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src")
params_dict = { \
        'a': 0.02, 'c': -65.0, 'b': 0.25, 'd': 2.0, 'i_offset': 0.73,
        'u_init': -14.0, 'v_init': -70.0}
pop_ex = p.Population(1, p.extra_models.IZK_curr_comb_exp_4E4I, params_dict, label="test")

d = 1
w = 1

# AMPA
# pop_ex.set('exc_a_tau', 0.5)
# pop_ex.set('exc_b_tau', 2.4)
# w = 0.1
# t_run = 30

# GABA_A
# pop_ex.set('exc_a_tau', 1)
# pop_ex.set('exc_b_tau', 7)
# w = 0.33
# t_run = 40

# GABA_B
# pop_ex.set('exc_a_tau', 60)
# pop_ex.set('exc_b_tau', 200)
# w = 0.0132
# t_run = 1750

# # NMDA
# pop_ex.set('exc_a_tau', 4)
# pop_ex.set('exc_b_tau', 40)
# w = 0.075
# t_run = 250

# # 5-HT-1A
# pop_ex.set('exc_a_tau', 210)
# pop_ex.set('exc_b_tau', 231)
# w = 0.0275
# t_run = 2600

# 5-HT-2A
# pop_ex.set('exc_a_tau', 3.25)
# pop_ex.set('exc_b_tau', 3.575)
# w = 0.2
# t_run = 300

# 5-HT-3A
pop_ex.set('exc_a_tau', 0.175)
pop_ex.set('exc_b_tau', 0.1925)
w = 0.310
t_run = 15



#
exc_proj = p.Projection(pop_src, pop_ex,
        p.OneToOneConnector(weights=w, delays=1*d), target="excitatory", label="projTemp")
# exc_proj2 = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=3*d), target="excitatory2")
# exc_proj3 = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=5*d), target="excitatory3")
# exc_proj4 = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=7*d), target="excitatory4")

# inh_proj = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=2*d), target="inhibitory")
# inh_proj2 = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=4*d), target="inhibitory2")
# inh_proj3 = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=6*d), target="inhibitory3")
# inh_proj4 = p.Projection(pop_src, pop_ex,
#         p.OneToOneConnector(weights=1, delays=8*d), target="inhibitory4")


pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
p.run(t_run)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"