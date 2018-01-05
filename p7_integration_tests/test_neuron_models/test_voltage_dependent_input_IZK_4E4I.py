import spynnaker7.pyNN as p
import plot_utils

p.setup(0.1)
runtime = 750
populations = []

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [105, 110, 115, 120, 125]#, 485]
                                         }, label="src1")
pop_src2 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [460]#, 465, 470, 475, 480]
                         }, label="src2")

cell_params = { # L_V_Py
        'a': 0.01, 'c': -65.0, 'b': 0.2, 'd': 8.0, 'i_offset': 3.83,
        'u_init': -14.0, 'v_init': -70.0,

        'exc_a_tau': 0.5, 'exc_b_tau': 2.4, # AMPA
        'exc2_a_tau': 0.5, 'exc2_b_tau': 2.4, # NMDA
        'exc3_a_tau': 0.5, 'exc3_b_tau': 2.4, # NMDA
        'exc4_a_tau': 4, 'exc4_b_tau': 40} # NMDA


pop_ex = p.Population(1, p.extra_models.IZK_curr_comb_exp_4E4I, cell_params,  label="test")

# define projections
exc_proj0 = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=1, delays=1), target="excitatory3")

exc_proj1 = p.Projection(pop_src1, pop_ex,
        p.OneToOneConnector(weights=2, delays=100), target="excitatory2")

# NMDA synapse
exc_proj2 = p.Projection(pop_src2, pop_ex,
        p.OneToOneConnector(weights=2, delays=1), target="excitatory4")

pop_ex.record()
pop_ex.record_gsyn()
pop_ex.record_v()

p.run(runtime)

v = pop_ex.get_v()
curr = pop_ex.get_gsyn()
spikes = pop_ex.getSpikes()

plot_utils.plotAll(v, spikes)
plot_utils.plot_gsyn(curr)

p.end()