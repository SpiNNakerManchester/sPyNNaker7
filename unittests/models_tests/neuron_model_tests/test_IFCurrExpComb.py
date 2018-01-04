import spynnaker7.pyNN as p
import python.plot_utils as plot_utils
p.setup(0.1)

pop_ex = p.Population(1, p.extra_models.IF_curr_comb_exp, {}, label="test")
pop_src1 = p.Population(1, p.SpikeSourceArray, {'spike_times': [[0]]}, label="src1")
p.set_number_of_neurons_per_core("IF_curr_comb_exp", 27)

# AMPA/ GABA_A
# pop_ex.set('exc_a_tau', 1.235)
# pop_ex.set('exc_b_tau', 1.3585)
# pop_ex.set('inh_a_tau', 1.235)
# pop_ex.set('inh_b_tau', 1.3585)
# t_run = 15

# # NMDA
# pop_ex.set('exc_a_tau', 18.5227)
# pop_ex.set('exc_b_tau', 20.375)
# pop_ex.set('inh_a_tau', 18.5227)
# pop_ex.set('inh_b_tau', 20.375)
# t_run = 250

# # 5-HT-1A
# pop_ex.set('exc_a_tau', 15.435)
# pop_ex.set('exc_b_tau', 16.9785)
# pop_ex.set('inh_a_tau', 15.435)
# pop_ex.set('inh_b_tau', 16.9785)
# t_run = 100

# 5-HT-2A
# pop_ex.set('exc_a_tau', 61.742)
# pop_ex.set('exc_b_tau', 67.9162)
# pop_ex.set('inh_a_tau', 61.742)
# pop_ex.set('inh_b_tau', 67.9162)
# t_run = 300

# 5-HT-3A
# pop_ex.set('exc_a_tau', 0.625)
# pop_ex.set('exc_b_tau', 0.6875)
# pop_ex.set('inh_a_tau', 0.625)
# pop_ex.set('inh_b_tau', 0.6875)
# t_run = 15


# define the projections
exc_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=2.2), target="excitatory")

inh_proj = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=5.5), target="inhibitory")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()
# p.run(225000)
p.run(t_run)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)
p.end()
print "\n job done"